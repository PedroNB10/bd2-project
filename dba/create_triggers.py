def create_trigger_payload(cur):
    try:
        # Cria a função que ignora a linha inválida
        cur.execute(
            '''
            CREATE OR REPLACE FUNCTION check_launch_exists()
            RETURNS TRIGGER AS $$
            BEGIN
                -- Verifica se o launch_id existe na tabela launches
                IF NOT EXISTS (SELECT 1 FROM launches WHERE id = NEW.launch_id) THEN
                    -- Registra um aviso para ser mostrado dps no load_database na função insert_payloads
                    RAISE NOTICE 'Launch ID % não encontrado. Inserção do payload % ignorada.', NEW.launch_id, NEW.id;
                    
                    -- Cancela a operação de inserção
                    RETURN NULL;
                END IF;
                
                -- Se o launch_id existe, permite a inserção
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
            '''
        )

        # Cria o trigger
        cur.execute(
            '''
            DROP TRIGGER IF EXISTS check_launch_exists ON payloads;
            
            -- Cria o trigger que executa a função antes de cada inserção na tabela payloads
            CREATE TRIGGER trg_check_launch_before_insert
            BEFORE INSERT ON payloads
            FOR EACH ROW
            EXECUTE FUNCTION check_launch_exists();
            '''
        )
        
    except Exception as e:
        print(f"Falha ao criar trigger: {e}")