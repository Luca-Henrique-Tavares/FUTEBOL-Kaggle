#!/usr/bin/env python3
"""
Script para combinar múltiplos notebooks Jupyter em um único notebook.
Ordem: analise.ipynb -> knn_predicao_colocacao.ipynb -> knn_premierleague.ipynb
"""

import nbformat
import os

def combinar_notebooks(notebooks_paths, output_path):
    """
    Combina múltiplos notebooks em um único notebook.
    
    Args:
        notebooks_paths (list): Lista com os caminhos dos notebooks a serem combinados
        output_path (str): Caminho onde salvar o notebook combinado
    """
    
    # Criar um novo notebook vazio
    combined_nb = nbformat.v4.new_notebook()
    
    # Adicionar célula de título inicial
    title_cell = nbformat.v4.new_markdown_cell("""# Análise Completa de Futebol - Kaggle

Este notebook combina toda a análise de dados de futebol, desde o processamento inicial dos dados até a aplicação de algoritmos de machine learning para predição de colocações.

## Estrutura:
1. **Análise e Processamento de Dados** - Limpeza e preparação dos datasets
2. **Preparação para Predição** - Organização dos dados para machine learning  
3. **Aplicação do KNN** - Modelo de predição usando K-Nearest Neighbors

---
""")
    combined_nb.cells.append(title_cell)
    
    # Para cada notebook na lista
    for i, notebook_path in enumerate(notebooks_paths):
        print(f"Processando: {notebook_path}")
        
        # Verificar se o arquivo existe
        if not os.path.exists(notebook_path):
            print(f"❌ Arquivo não encontrado: {notebook_path}")
            continue
            
        try:
            # Ler o notebook
            with open(notebook_path, 'r', encoding='utf-8') as f:
                nb = nbformat.read(f, as_version=4)
            
            # Adicionar célula de separação com título da seção
            section_titles = [
                "# Parte 1: Análise e Processamento de Dados",
                "# Parte 2: Preparação para Predição de Colocações", 
                "# Parte 3: Aplicação do Algoritmo KNN"
            ]
            
            if i < len(section_titles):
                section_cell = nbformat.v4.new_markdown_cell(f"\n---\n\n{section_titles[i]}\n\n---\n")
                combined_nb.cells.append(section_cell)
            
            # Adicionar todas as células do notebook atual
            for cell in nb.cells:
                # Criar uma nova célula baseada no tipo
                if cell.cell_type == 'markdown':
                    new_cell = nbformat.v4.new_markdown_cell(cell.source)
                elif cell.cell_type == 'code':
                    new_cell = nbformat.v4.new_code_cell(cell.source)
                else:
                    # Para outros tipos de célula (raw, etc.)
                    new_cell = cell.copy()
                
                # Copiar metadados se existirem
                if hasattr(cell, 'metadata'):
                    new_cell.metadata = cell.metadata
                
                # Adicionar ao notebook combinado
                combined_nb.cells.append(new_cell)
                
            print(f"✅ {len(nb.cells)} células adicionadas de {os.path.basename(notebook_path)}")
            
        except Exception as e:
            print(f"❌ Erro ao processar {notebook_path}: {str(e)}")
            continue
    
    # Salvar o notebook combinado
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            nbformat.write(combined_nb, f)
        print(f"\n🎉 Notebook combinado salvo em: {output_path}")
        print(f"📊 Total de células: {len(combined_nb.cells)}")
        
    except Exception as e:
        print(f"❌ Erro ao salvar o notebook: {str(e)}")

def main():
    """Função principal"""
    
    # Definir os caminhos dos notebooks (na ordem especificada)
    notebooks = [
        "analise.ipynb",
        "knn_predicao_colocacao.ipynb", 
        "knn_premierleague.ipynb"
    ]
    
    # Nome do arquivo de saída
    output_notebook = "analise_completa_futebol.ipynb"
    
    print("🚀 Iniciando combinação dos notebooks...")
    print(f"📝 Notebooks a combinar: {notebooks}")
    print(f"📄 Arquivo de saída: {output_notebook}")
    print("-" * 50)
    
    # Combinar os notebooks
    combinar_notebooks(notebooks, output_notebook)

if __name__ == "__main__":
    main()
