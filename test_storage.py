from src.models import Opportunity
from src.storage import get_opportunities, save_opportunity, init_db


def main():
        print("1. Inicializando o banco...")
        init_db()
  
        print("2. Criando oportunidade de teste...")
        opp = Opportunity(
            title = "Edital Preservação da Memória e Museus 2026",
            agency_name = "Ministério da Cultura",
            source_url = "https://gov.br/cultura/edital-museus-2026",
            submission_deadline = "2026-12-01",
            max_budget = 150000.00,
            score = 5,
            justification = "Diretamente alinhado com a digitalização de acervo do Museu do Fogo."
        )   
  
        print("3. Salvando no SQLite...")
        save_opportunity(opp)
  
        print("4. Consultando oportunidades salvas...")
        items = get_opportunities()
        print(f"Total encontrado no banco: {len(items)}")
        
        for item in items:
            print(f"-> [{item.score}/5] {item.title} ({item.agency_name})")
  
if __name__ == "__main__":
    main()