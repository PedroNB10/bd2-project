import React, { useEffect, useRef, useState } from 'react';
import axios from 'axios';
import Select from 'react-select';

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


const operadoresPorTipo: Record<string, string[]> = {
    integer: ['igual a', 'maior que', 'menor que', 'maior ou igual a', 'menor ou igual a', 'entre'],
    float: ['igual a', 'maior que', 'menor que', 'maior ou igual a', 'menor ou igual a', 'entre'],
    double: ['igual a', 'maior que', 'menor que', 'maior ou igual a', 'menor ou igual a', 'entre'],
    date: ['igual a', 'maior que', 'menor que', 'maior ou igual a', 'menor ou igual a', 'entre'],
    varchar: ['igual a', 'parecido com'],
    text: ['igual a', 'parecido com'],
    boolean: ['igual a', 'diferente de']
};


const RelatorioAdHoc: React.FC = () => {
    const [tabelasSelecionadas, setTabelasSelecionadas] = useState<string[]>([]);
    const [colunasDisponiveis, setColunasDisponiveis] = useState<ColunaDisponivel[]>([]);
    const [colunasSelecionadas, setColunasSelecionadas] = useState<string[]>([]);
    const [dados, setDados] = useState<DadosAPI[]>([]);
    const [filtros, setFiltros] = useState<Filtro[]>([]);


    const obterTipoColuna = (colunaNome: string): string => {
        const found = colunasDisponiveis.find(c => c.nome === colunaNome);
        return found?.tipo || 'varchar';
    };

    const obterOperadores = (tipo: string): string[] => {
        return operadoresPorTipo[tipo] || ['='];
    };

    const adicionarFiltro = () => {
        setFiltros([...filtros, { coluna: '', tipo: '', operador: '=', valor: '' }]);
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
        'rockets', 'cores', 'orbitals', 'crew',
        'launchpads', 'launches', 'launchcores',
        'payloads', 'starlinksatellites'
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
                        .get<[string, string][]>(`http://192.168.1.103:3000/api/${tabela}/columns`)
                        .then(res => res.data.map(([col, tipo]) => ({
                            nome: `${tabela}_${col}`,
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
                prev.filter(col => !removidas.some(tab => col.nome.startsWith(`${tab}_`)))
            );
            setColunasSelecionadas(prev =>
                prev.filter(col => !removidas.some(tab => col.startsWith(`${tab}_`)))
            );
        }
    }, [tabelasSelecionadas]);

    // const buscarDados = () => {
    //     const estrutura = {
    //         tabelas: tabelasSelecionadas,
    //         colunas: colunasSelecionadas.map(col => {
    //             const [tabela, ...resto] = col.split('_');
    //             return `${tabela}.${resto.join('_')}`;
    //         }),
    //         filtros: filtros
    //             .filter(f => f.coluna && f.operador && f.valor !== '')
    //             .map(f => ({
    //                 coluna: f.coluna.replace('_', '.'),
    //                 operador: f.operador,
    //                 valor: f.valor
    //             }))
    //     };

    //     console.log('🔍 Estrutura pronta para o back:');
    //     console.log(JSON.stringify(estrutura, null, 2));




    // };
    const buscarDados = () => {
        const estrutura = {
            tabelas: tabelasSelecionadas,
            colunas: colunasSelecionadas.map(col => {
                const [tabela, ...resto] = col.split('_');
                return `${tabela}.${resto.join('_')}`;
            }),
            filtros: filtros
                .filter(f => f.coluna && f.operador && f.valor !== '')
                .map(f => ({
                    coluna: f.coluna.replace('_', '.'),
                    operador: f.operador,
                    valor: f.valor
                }))
        };

        console.log('🔍 Estrutura pronta para o back:');
        console.log(JSON.stringify(estrutura, null, 2));

        axios.post('/api/relatorio', estrutura)
            .then(response => {
                setDados(response.data); // atualiza estado com dados recebidos
                console.log('Dados recebidos:', response.data);
            })
            .catch(error => {
                console.error('Erro ao buscar dados:', error);
                setDados([]); // limpa dados em caso de erro
            });
    };


    return (
        <div>
            <h2>Relatório Ad Hoc</h2>

            <label>Tabelas:</label>
            <Select
                isMulti
                options={tabelas
                    // Se nenhuma tabela foi selecionada OU 'launches' está entre as selecionadas → mostra tudo
                    .filter(tabela => {
                        return (
                            tabelasSelecionadas.length === 0 ||
                            tabelasSelecionadas.includes('launches') ||
                            tabelasSelecionadas.includes(tabela) || // mantém as já selecionadas
                            tabela === 'launches' // permite adicionar launches
                        );
                    })
                    .map(t => ({ label: t, value: t }))
                }
                value={tabelasSelecionadas.map(t => ({ label: t, value: t }))}
                onChange={(selectedOptions) => {
                    const valores = selectedOptions.map(opt => opt.value);

                    // Se o usuário de alguma forma burlar e selecionar várias tabelas sem launches, limpa
                    if (valores.length > 1 && !valores.includes('launches')) {
                        // Opcional: aqui você pode alertar ou corrigir
                        setTabelasSelecionadas([valores[0]]);
                        return;
                    }

                    setTabelasSelecionadas(valores);
                }}
                placeholder="Selecione tabelas..."
                styles={customStyles}
            />

            {colunasDisponiveis.length > 0 && (
                <>
                    <label>Atributos:</label>
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

                    <div style={{ marginTop: '1rem' }}>
                        <h4>Filtros</h4>
                        {filtros.map((filtro, i) => {
                            const tipo = obterTipoColuna(filtro.coluna);
                            const operadoresDisponiveis = obterOperadores(tipo);

                            return (
                                <div key={i} style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.5rem' }}>
                                    <Select
                                        options={colunasSelecionadas.map(col => ({
                                            label: col,
                                            value: col
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

                                    <Select
                                        options={operadoresDisponiveis.map(op => ({ label: op, value: op }))}
                                        value={{ label: filtro.operador, value: filtro.operador }}
                                        onChange={(opt) => atualizarFiltro(i, 'operador', opt?.value || '=')}
                                        placeholder="Operador"
                                        styles={customStyles}
                                    />

                                    {filtro.operador === 'BETWEEN' ? (
                                        <>
                                            <input
                                                type="number"
                                                placeholder="Min"
                                                onChange={(e) => {
                                                    const val = filtro.valor as [number, number] || [0, 0];
                                                    atualizarFiltro(i, 'valor', [Number(e.target.value), val[1]]);
                                                }}
                                            />
                                            <input
                                                type="number"
                                                placeholder="Max"
                                                onChange={(e) => {
                                                    const val = filtro.valor as [number, number] || [0, 0];
                                                    atualizarFiltro(i, 'valor', [val[0], Number(e.target.value)]);
                                                }}
                                            />
                                        </>
                                    ) : tipo === 'integer' || tipo === 'float' || tipo === 'double' ? (
                                        <input
                                            type="number"
                                            placeholder="Valor"
                                            value={typeof filtro.valor === 'number' ? filtro.valor : ''}
                                            onChange={(e) => atualizarFiltro(i, 'valor', Number(e.target.value))}
                                        />
                                    ) : tipo === 'boolean' ? (
                                        <select
                                            value={String(filtro.valor)}
                                            onChange={(e) => atualizarFiltro(i, 'valor', e.target.value === 'true')}
                                        >
                                            <option value="true">Verdadeiro</option>
                                            <option value="false">Falso</option>
                                        </select>
                                    ) : (
                                        <input
                                            type="text"
                                            placeholder="Valor"
                                            value={typeof filtro.valor === 'string' ? filtro.valor : ''}
                                            onChange={(e) => atualizarFiltro(i, 'valor', e.target.value)}
                                        />
                                    )}

                                    <button onClick={() => removerFiltro(i)}>X</button>
                                </div>
                            );
                        })}

                        <button onClick={adicionarFiltro}>Adicionar Filtro</button>
                    </div>

                    <button onClick={buscarDados}>Buscar</button>
                </>
            )}

            {dados.length > 0 && (
                <table>
                    <thead>
                        <tr>
                            {Object.keys(dados[0]).map((col, i) => (
                                <th key={i}>{col}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {dados.map((linha, i) => (
                            <tr key={i}>
                                {Object.keys(dados[0]).map((col, j) => (
                                    <td key={j}>{linha[col]}</td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}

        </div>
    );
};

export default RelatorioAdHoc;
