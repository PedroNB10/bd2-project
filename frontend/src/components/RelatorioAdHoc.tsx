import React, { useEffect, useRef, useState } from 'react';
import axios from 'axios';
import Select from 'react-select';
import DataTable from 'react-data-table-component';
import { CSVLink } from 'react-csv';
import { toast } from 'react-toastify';
import rocketLoader from '../assets/rocket-loader.gif'; // caminho relativo ao seu componente

interface Filtro {
    coluna: string;
    tipo: string;
    operador: string;
    valor: string | number | [number, number] | boolean;
}

interface ColunaDisponivel {
    nome: string;
    tipo: string;
}

interface DadosAPI {
    [key: string]: any;
}

interface Agregacao {
    coluna: string;
    funcao: string;
    alias?: string;
    having?: {
        operador: string;
        valor: number;
    };
}


const operadoresPorTipo: Record<string, string[]> = {
    integer: ['igual a', 'maior que', 'menor que', 'maior ou igual a', 'menor ou igual a', 'entre'],
    float: ['igual a', 'maior que', 'menor que', 'maior ou igual a', 'menor ou igual a', 'entre'],
    double: ['igual a', 'maior que', 'menor que', 'maior ou igual a', 'menor ou igual a', 'entre'],
    date: ['igual a', 'maior que', 'menor que', 'maior ou igual a', 'menor ou igual a', 'entre'],
    varchar: ['igual a', 'parecido com'],
    text: ['igual a', 'parecido com'],
    boolean: ['igual a', 'diferente de'],
    datetime: ['entre']
};


const operadoresHaving = [

    { value: '', label: 'Selecione (opcional)' },
    { value: '>', label: 'Maior' },
    { value: '>=', label: 'Maior igual' },
    { value: '<', label: 'Menor' },
    { value: '<=', label: 'Menor igual' },
    { value: '=', label: 'Igual' },
    { value: '!=', label: 'Diferente' },
];

const funcoesAgregacao =[
    { value: '', label: 'Selecione...' },
    { value: 'COUNT', label: 'Número de repetições' },
    { value: 'SUM', label: 'Somatório' },
    { value: 'AVG', label: 'Média' },
    { value: 'MIN', label: 'Mínimo' },
    { value: 'MAX', label: 'Máximo' },
]


const RelatorioAdHoc: React.FC = () => {
    const [carregando, setCarregando] = useState(false);
    const [tabelasSelecionadas, setTabelasSelecionadas] = useState<string[]>([]);
    const [colunasDisponiveis, setColunasDisponiveis] = useState<ColunaDisponivel[]>([]);
    const [colunasSelecionadas, setColunasSelecionadas] = useState<string[]>([]);
    const [dados, setDados] = useState<DadosAPI[]>([]);
    const [filtros, setFiltros] = useState<Filtro[]>([]);
    const [agregacoes, setAgregacoes] = useState<Agregacao[]>([]);
    const alertError = (msg: string) => {
        toast.error(msg);
    };
    const obterTipoColuna = (colunaNome: string): string => {
        const found = colunasDisponiveis.find(c => c.nome === colunaNome);
        return found?.tipo || 'varchar';
    };

    const adicionarAgregacao = () => {
        setAgregacoes([...agregacoes, { coluna: '', funcao: 'COUNT' }]);
    };

    const atualizarAgregacao = (index: number, campo: keyof Agregacao, valor: any) => {
        const novas: any = [...agregacoes];
        novas[index][campo] = valor;
        setAgregacoes(novas);
    };

    const atualizarHaving = (index: number, campo: 'operador' | 'valor', valor: any) => {
        const novas: any = [...agregacoes];
        if (!novas[index].having)
            novas[index].having = { operador: '>', valor: 0 };
        novas[index].having![campo] = valor;
        setAgregacoes(novas);
    };

    const removerAgregacao = (index: number) => {
        setAgregacoes(agregacoes.filter((_, i) => i !== index));
    };


    const obterOperadores = (tipo: string): string[] => {
        return operadoresPorTipo[tipo] || ['='];
    };

    const adicionarFiltro = () => {
        setFiltros([...filtros, { coluna: '', tipo: '', operador: 'Selecione...', valor: '' }]);
    };

    const atualizarFiltro = (index: number, campo: keyof Filtro, novoValor: any) => {
        const novos = [...filtros];
        novos[index][campo] = novoValor;
        setFiltros(novos);
    };

    const removerFiltro = (index: number) => {
        setFiltros(filtros.filter((_, i) => i !== index));
    };

    const customStyles = {
        control: (provided: any) => ({
            ...provided,
            backgroundColor: '#f2f2f2',
            borderColor: '#999',
            minHeight: '38px',
            fontSize: '14px',
        }),
        option: (provided: any, state: any) => ({
            ...provided,
            backgroundColor: state.isSelected
                ? '#007BFF'
                : state.isFocused
                    ? '#e6f0ff'
                    : 'white',
            color: state.isSelected ? 'white' : 'black',
            padding: 10,
            cursor: 'pointer',
        }),
        multiValue: (provided: any) => ({
            ...provided,
            backgroundColor: '#007BFF',
            borderRadius: '4px',
            color: 'white',
        }),
        multiValueLabel: (provided: any) => ({
            ...provided,
            color: 'white',
            fontWeight: 'bold',
        }),
        multiValueRemove: (provided: any) => ({
            ...provided,
            color: 'white',
            ':hover': {
                backgroundColor: '#0056b3',
                color: 'white',
            },
        }),
    };

    const tabelas: string[] = [
        'rockets', 'cores', 'orbital_parameters', 'crew',
        'launchpads', 'launches', 'launch_cores',
        'payloads', 'starlink_satellites'
    ];

    const prevTabelas = useRef<string[]>([]);

    useEffect(() => {
        const tabelasAtuais = new Set(tabelasSelecionadas);
        const tabelasAntigas = new Set(prevTabelas.current);

        const adicionadas = tabelasSelecionadas.filter(t => !tabelasAntigas.has(t));
        const removidas = prevTabelas.current.filter(t => !tabelasAtuais.has(t));

        prevTabelas.current = tabelasSelecionadas;

        if (adicionadas.length === 0 && removidas.length === 0) return;

        if (adicionadas.length > 0) {
            Promise.all(
                adicionadas.map(tabela =>
                    axios
                        .get<[string, string][]>(`/api/${tabela}/columns`)
                        .then(res => res.data.map(([col, tipo]) => ({
                            nome: `${tabela}/${col}`,
                            tipo: tipo.toLowerCase()
                        })))
                        .catch(err => {
                            console.error(`Erro ao buscar colunas da tabela ${tabela}:`, err);
                            return [];
                        })
                )
            ).then(novasColunasListas => {
                const novasColunas = novasColunasListas.flat();
                setColunasDisponiveis(prev => Array.from(new Set([...prev, ...novasColunas])));
            });
        }

        if (removidas.length > 0) {
            setColunasDisponiveis(prev =>
                prev.filter(col => !removidas.some(tab => col.nome.startsWith(`${tab}/`)))
            );
            setColunasSelecionadas(prev =>
                prev.filter(col => !removidas.some(tab => col.startsWith(`${tab}/`)))
            );
        }
    }, [tabelasSelecionadas]);

    const buscarDados = () => {
        setCarregando(true); // Ativa o GIF

        const estrutura = {
            tabelas: tabelasSelecionadas,
            colunas: colunasSelecionadas.map(col => {
                const [tabela, ...resto] = col.split('/');
                return `${tabela}.${resto.join('_')}`;
            }),
            filtros: filtros
                .filter(f => f.coluna && f.operador && f.valor !== '')
                .map(f => ({
                    coluna: f.coluna.replace('/', '.'),
                    operador: f.operador,
                    valor: f.valor
                })),
            agregacoes: agregacoes.map(agg => ({
                coluna: agg.coluna.replace('/', '.'),
                funcao: agg.funcao,
                alias: agg.alias ? agg.alias : agg.coluna.replace('/', '.') + " (" + agg.funcao + ")",
                having: agg.having
            }))
        };

        console.log('Estrutura pronta para o back:');
        console.log(JSON.stringify(estrutura, null, 2));

        axios.post('/api/relatorio', estrutura)
            .then(response => {
                setDados(response.data); // atualiza estado com dados recebidos
                console.log('Dados recebidos:', response.data);
            })
            .catch(error => {
                console.error('Erro ao buscar dados:', error);
                alertError('Erro ao buscar dados:')

                setDados([]); // limpa dados em caso de erro
            }) 
            .finally(() => {
                setCarregando(false); // Desativa o GIF
            });
    };

    const colunasTabela = dados.length > 0
        ? Object.keys(dados[0]).map(col => ({
            name: String(col),
            selector: (row: any) => String(row[col]),
            sortable: true,
        }))
        : [];

    const podeSelecionarTabela = function (tabela: string, selecionadas: string[]) {
        if (selecionadas.length === 0) return true;

        // Mantém visível as já selecionadas
        if (selecionadas.includes(tabela)) return true;
        
        if (selecionadas.includes('cores') && selecionadas.length === 1) {
            return tabela === 'launch_cores';
        }

        if (selecionadas.includes('orbital_parameters') && selecionadas.length === 1) {
            // Orbital_parameters só se conecta com starlink_satellites
            return tabela === 'starlink_satellites';
        }

        if (selecionadas.includes('starlink_satellites') && selecionadas.length === 1) {
            // Starlink_Satellites pode ir com orbital_parameters ou launches
            return tabela === 'orbital_parameters' || tabela === 'launches';
        }

        if (selecionadas.includes('launches')) {
            if (tabela === 'orbital_parameters') {
                // Orbital_parameters só aparece se starlink_satellites estiver também
                return selecionadas.includes('starlink_satellites');
            }

            // Qualquer outra tabela é permitida
            return true;
        }

        // Qualquer outra primeira tabela → só permite launches como segunda
        return tabela === 'launches';
    }

    return (
        <div className="d-block h-full min-vh-100">
            <div className='w-100 d-flex justify-content-center'>
                {/* <h2>Relatório Ad Hoc</h2> */}
                <div className="card mt-5 p-3 w-75">
                    <h5>Tabelas:</h5>

                    <Select
                        isMulti
                        options={tabelas
                            .filter(t => podeSelecionarTabela(t, tabelasSelecionadas))
                            .map(t => ({ label: t, value: t }))
                        }
                        value={tabelasSelecionadas.map(t => ({ label: t, value: t }))}
                        onChange={(selectedOptions) => {
                            const valores = selectedOptions.map(opt => opt.value);
                            setTabelasSelecionadas(valores);
                        }}
                        placeholder="Selecione tabelas..."
                        styles={customStyles}
                    />

                    {colunasDisponiveis.length > 0 && (
                        <>
                            <h5>Atributos:</h5>
                            <Select
                                isMulti
                                styles={customStyles}
                                options={colunasDisponiveis.map(col => ({
                                    label: col.nome,
                                    value: col.nome
                                }))}
                                value={colunasSelecionadas.map(col => ({
                                    label: col,
                                    value: col
                                }))}
                                onChange={(selectedOptions) => {
                                    const valores = selectedOptions.map(opt => opt.value);
                                    setColunasSelecionadas(valores);
                                }}
                                placeholder="Selecione colunas..."
                            />

                            <div className='mt-1 form-group '>
                                <h5>Agregações</h5>
                                {agregacoes.map((agg, i) => (
                                    <div key={i} className='d-flex col-md-12 mt-1'>
                                        {/* Coluna (somente das já selecionadas) */}
                                        <div className='col-md-3 me-3'>
                                            <Select
                                                options={colunasSelecionadas.map(col => ({ label: col, value: col }))}
                                                value={agg.coluna ? { label: agg.coluna, value: agg.coluna } : null}
                                                onChange={(opt) => atualizarAgregacao(i, 'coluna', opt?.value)}
                                                placeholder="Coluna"
                                                styles={customStyles}

                                            />
                                        </div>

                                        {/* Função agregada */}
                                        <div className='col-md me-3'>
                                            <Select
                                                // options={['COUNT', 'SUM', 'AVG', 'MIN', 'MAX'].map(func => ({
                                                //     label: func, value: func
                                                // }))}
                                                options={funcoesAgregacao}
                                                // value={{ label: agg.funcao, value: agg.funcao }}
                                                value={operadoresHaving.find(opt => opt.value === (agg?.funcao || ''))}
                                                onChange={(opt) => atualizarAgregacao(i, 'funcao', opt?.value)}
                                                placeholder="Função"
                                                styles={customStyles}
                                            />
                                        </div>

                                        {/* Alias */}
                                        <div className='col-md-3 me-3'>
                                            <input
                                                type="text"
                                                className="form-control"
                                                placeholder="Nome da tabela adicionada (opcional)"
                                                value={agg.alias || ''}
                                                onChange={(e) => atualizarAgregacao(i, 'alias', e.target.value)}
                                            />
                                        </div>

                                        {/* HAVING opcional */}
                                        <div className='col-md me-3'>
                                            <Select
                                                options={operadoresHaving}
                                                value={operadoresHaving.find(opt => opt.value === (agg.having?.operador || ''))}
                                                onChange={(opt) => atualizarHaving(i, 'operador', opt?.value || '')}
                                                placeholder="Operador"
                                                styles={customStyles}
                                            />
                                        </div>
                                        <div className='col-md me-3'>
                                            <input
                                                type="number"
                                                className="form-control"
                                                placeholder="Valor"
                                                value={agg.having?.valor || ''}
                                                onChange={(e) => atualizarHaving(i, 'valor', Number(e.target.value))}
                                            />
                                        </div>

                                        <button className="btn btn-danger" onClick={() => removerAgregacao(i)}>X</button>

                                    </div>
                                ))}
                                <button className="btn mt-2 btn-primary" onClick={adicionarAgregacao}>Adicionar Agregação</button>
                            </div>

                            <div className='mt-1 form-group'>
                                <h5>Filtros</h5>
                                {filtros.map((filtro, i) => {
                                    const tipo = obterTipoColuna(filtro.coluna);
                                    const operadoresDisponiveis = obterOperadores(tipo);

                                    return (
                                        <div key={i} className='d-flex col-md-12 mt-1'>
                                            <div className='col-md-3 me-3'>
                                                <Select
                                                    options={colunasDisponiveis.map(col => ({
                                                        label: col.nome,
                                                        value: col.nome
                                                    }))}
                                                    value={filtro.coluna ? { label: filtro.coluna, value: filtro.coluna } : null}
                                                    onChange={(opt) => {
                                                        const tipoCol = obterTipoColuna(opt?.value || '');
                                                        atualizarFiltro(i, 'coluna', opt?.value || '');
                                                        atualizarFiltro(i, 'tipo', tipoCol);
                                                    }}
                                                    placeholder="Coluna"
                                                    styles={customStyles}
                                                />
                                            </div>
                                            <div className='col-md me-3'>
                                                <Select
                                                    options={operadoresDisponiveis.map(op => ({ label: op, value: op }))}
                                                    value={{ label: filtro.operador, value: filtro.operador }}
                                                    onChange={(opt) => atualizarFiltro(i, 'operador', opt?.value || '=')}
                                                    placeholder="Operador"
                                                    styles={customStyles}
                                                />
                                            </div>

                                            {filtro.operador === 'entre' && (tipo === 'integer' || tipo === 'float' || tipo === 'double') ? (
                                                <div className='col-md-5 me-3 d-flex '>
                                                    <div className='col-md me-3'>
                                                        <input
                                                            type="number"
                                                            placeholder="Min"
                                                            className="form-control me-3"
                                                            onChange={(e) => {
                                                                const val = filtro.valor as [number, number] || [0, 0];
                                                                atualizarFiltro(i, 'valor', [Number(e.target.value), val[1]]);
                                                            }}
                                                        />
                                                    </div>
                                                    <div className="col-md">
                                                        <input
                                                            type="number"
                                                            placeholder="Max"
                                                            className="form-control me-3"
                                                            onChange={(e) => {
                                                                const val = filtro.valor as [number, number] || [0, 0];
                                                                atualizarFiltro(i, 'valor', [val[0], Number(e.target.value)]);
                                                            }}
                                                        />
                                                    </div>
                                                </div>
                                            ) : tipo === 'integer' || tipo === 'float' || tipo === 'double' ? (
                                                <div className='col-md-5 me-3'>
                                                    <input
                                                        type="number"
                                                        className="form-control"
                                                        placeholder="Valor"
                                                        value={typeof filtro.valor === 'number' ? filtro.valor : ''}
                                                        onChange={(e) => atualizarFiltro(i, 'valor', Number(e.target.value))}
                                                    />
                                                </div>
                                            ) : tipo === 'boolean' ? (
                                                <div className='col-md-5 me-3'>
                                                    <Select
                                                        options={[
                                                            { label: 'Verdadeiro', value: 'true' },
                                                            { label: 'Falso', value: 'false' }
                                                        ]}
                                                        value={
                                                            filtro.valor !== undefined
                                                                ? { label: filtro.valor ? 'Verdadeiro' : 'Falso', value: String(filtro.valor) }
                                                                : null
                                                        }
                                                        onChange={(opt) => atualizarFiltro(i, 'valor', opt?.value === 'true')}
                                                        placeholder="Valor"
                                                        styles={customStyles}
                                                    />
                                                </div>
                                            ) : tipo === 'datetime' && filtro.operador === 'entre' ? (
                                                <div className='d-flex col-md-5 me-3'>
                                                    <div className="col-md me-3">
                                                        <input
                                                            type="date"
                                                            className="form-control me-3"
                                                            value={Array.isArray(filtro.valor) ? filtro.valor[0] : ''}
                                                            onChange={(e) => {
                                                                const fim = Array.isArray(filtro.valor) ? filtro.valor[1] : '';
                                                                atualizarFiltro(i, 'valor', [e.target.value, fim]);
                                                            }}
                                                        />
                                                    </div>
                                                    <div className="col-md">
                                                        <input
                                                            type="date"
                                                            className="form-control me-3"
                                                            value={Array.isArray(filtro.valor) ? filtro.valor[1] : ''}
                                                            onChange={(e) => {
                                                                const inicio = Array.isArray(filtro.valor) ? filtro.valor[0] : '';
                                                                atualizarFiltro(i, 'valor', [inicio, e.target.value]);
                                                            }}
                                                        />
                                                    </div>
                                                </div>
                                            ) :
                                                (
                                                    <div className='col-md-5 me-3'>
                                                        <input
                                                            type="text"
                                                            className="form-control"
                                                            placeholder="Valor"
                                                            value={typeof filtro.valor === 'string' ? filtro.valor : ''}
                                                            onChange={(e) => atualizarFiltro(i, 'valor', e.target.value)}
                                                        />
                                                    </div>
                                                )}

                                            <button className="btn btn-danger" onClick={() => removerFiltro(i)}>X</button>
                                        </div>
                                    );
                                })}

                                <button className="btn mt-2 btn-primary" onClick={adicionarFiltro}>Adicionar Filtro</button>
                            </div>

                            <button className="btn mt-2 btn-primary" onClick={buscarDados}>Buscar</button>
                        </>
                    )}
                </div>
            </div>
            <div className='w-100 d-flex justify-content-center'>

                <div className='card mt-1 w-75'>
                    {carregando && (
                        <div className="text-center mt-4">
                            <img src={rocketLoader} alt="Carregando..." width="100" />
                            <p className="mt-2">Cabo Houston, estamos recebendo os dados!</p>
                        </div>
                    )}
                    {!carregando && (
                    <div className='d-flex justify-content-center'>
                        <div className='w-75'>
                            {dados.length > 0 && (
                                <>
                                    <div style={{ marginBottom: '1rem' }}>
                                        <CSVLink
                                            data={dados}
                                            filename="relatorio.csv"
                                            className="btn mt-2 btn-primary"
                                            target="_blank"
                                        >
                                            Exportar CSV
                                        </CSVLink>
                                    </div>
                                    <DataTable
                                        columns={colunasTabela}
                                        data={dados}
                                        pagination
                                        highlightOnHover
                                        responsive
                                        striped
                                    />
                                </>
                            )}
                        </div>
                    </div>
                    )}
                </div>
            </div>
            
        </div>
    );
};

export default RelatorioAdHoc;
