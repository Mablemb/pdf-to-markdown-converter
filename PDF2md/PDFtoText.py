import pymupdf4llm
import pathlib
import argparse
import os
import time
from tqdm import tqdm
import threading
import itertools
import sys

def spinner_animation(stop_event, message="Processando"):
    """
    Exibe um spinner (pontos piscantes) durante o processamento para indicar atividade.
    
    Args:
        stop_event: Evento para interromper a animação
        message: Mensagem a ser exibida antes do spinner
    """
    spinner = itertools.cycle(['.  ', '.. ', '...', '   '])
    while not stop_event.is_set():
        sys.stdout.write('\r' + message + next(spinner))
        sys.stdout.flush()
        time.sleep(0.8)
    # Limpar a linha quando terminar
    sys.stdout.write('\r' + ' ' * (len(message) + 4) + '\r')
    sys.stdout.flush()

def convert_pdf_to_markdown(input_path, output_path):
    """
    Converte um arquivo PDF para formato Markdown
    
    Args:
        input_path (str): Caminho/nome do arquivo PDF de entrada
        output_path (str): Caminho/nome onde o arquivo Markdown será salvo
    
    Returns:
        bool: True se a conversão foi bem-sucedida, False caso contrário
    """
    # Extrai o diretório do caminho de saída
    output_dir = os.path.dirname(output_path)
    
    # Verifica se o diretório de saída existe, se não, tenta criá-lo
    if output_dir and not os.path.exists(output_dir):
        try:
            print(f"Criando diretório de saída: {output_dir}")
            os.makedirs(output_dir, exist_ok=True)
        except PermissionError:
            print(f"\nERRO: Sem permissão para criar o diretório: {output_dir}")
            print("Sugestões:")
            print("1. Execute o script com privilégios de administrador")
            print("2. Escolha um diretório de saída onde você tenha permissões de escrita")
            print("3. Verifique se o diretório de saída não está sendo usado por outro processo")
            return False
        except Exception as e:
            print(f"\nERRO ao criar o diretório: {str(e)}")
            return False
    
    # Verifica se o diretório de saída tem permissões de escrita
    if output_dir and not os.access(output_dir, os.W_OK):
        print(f"\nERRO: Sem permissão de escrita no diretório: {output_dir}")
        print("Sugestões:")
        print("1. Execute o script com privilégios de administrador")
        print("2. Escolha um diretório de saída onde você tenha permissões de escrita")
        return False
    
    # Verifica se o arquivo de saída já existe dentro da pasta
    if os.path.isfile(output_path):
        print(f"Arquivo já existe na pasta de saída: {output_path}")
        print("Pulando conversão para evitar sobrescrita.")
        return False
    
    try:
        # Verifica se o arquivo de entrada existe
        if not os.path.isfile(input_path):
            print(f"\nERRO: O arquivo de entrada não existe: {input_path}")
            return False
            
        # Obtém informações iniciais sobre o arquivo PDF
        print(f"Iniciando conversão de: {input_path}")
        start_time = time.time()
        
        # Inicia o spinner para indicar atividade durante o processamento inicial
        stop_spinner = threading.Event()
        spinner_thread = threading.Thread(
            target=spinner_animation,
            args=(stop_spinner, "Analisando o PDF e preparando a conversão")
        )
        spinner_thread.daemon = True
        spinner_thread.start()
        
        try:
            # Converte o PDF para Markdown
            md_text = pymupdf4llm.to_markdown(input_path)
        except Exception as e:
            # Para o spinner se ocorrer um erro
            stop_spinner.set()
            spinner_thread.join()
            print(f"\nERRO durante a conversão do PDF: {str(e)}")
            return False
        
        # Para o spinner
        stop_spinner.set()
        spinner_thread.join()
        
        # Agora exibe a barra de progresso para o restante do processo
        with tqdm(total=100, desc="Finalizando a conversão", unit="%") as pbar:
            # Já concluímos a parte mais demorada, então começamos em 70%
            pbar.update(70)
            
            # Pausa para mostrar o progresso
            time.sleep(0.5)
            
            try:
                # Salva o conteúdo Markdown no arquivo de saída
                pathlib.Path(output_path).write_bytes(md_text.encode())
            except PermissionError:
                print(f"\nERRO: Sem permissão para escrever no arquivo: {output_path}")
                print("Sugestões:")
                print("1. Execute o script com privilégios de administrador")
                print("2. Escolha um diretório de saída onde você tenha permissões de escrita")
                return False
            except Exception as e:
                print(f"\nERRO ao salvar o arquivo: {str(e)}")
                return False
                
            pbar.update(15)
            
            # Pausa para mostrar o progresso
            time.sleep(0.3)
            
            # Completa a barra de progresso
            pbar.update(15)
        
        # Calcula o tempo total
        elapsed_time = time.time() - start_time
        
        print(f"Conversão concluída com sucesso em {elapsed_time:.2f} segundos")
        print(f"Arquivo de saída: {output_path}")
        return True
    except Exception as e:
        print(f"\nERRO durante a conversão: {str(e)}")
        return False

if __name__ == "__main__":
    # Configuração do parser de argumentos de linha de comando
    parser = argparse.ArgumentParser(description="Conversor de PDF para Markdown")
    parser.add_argument("input_path", help="Caminho/nome do arquivo PDF a ser convertido")
    parser.add_argument("output_path", help="Caminho/nome do arquivo Markdown de saída")
    
    # Analisa os argumentos da linha de comando
    args = parser.parse_args()
    
    # Chama a função de conversão
    convert_pdf_to_markdown(args.input_path, args.output_path)