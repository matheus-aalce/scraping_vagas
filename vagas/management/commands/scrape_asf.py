import requests
from bs4 import BeautifulSoup
from django.core.management import BaseCommand

from ...models import Vaga

ASF_BASE_URL = "https://www.saudedafamilia.org/_wp/index.php/pt/home"
PAGE_URL = "/recrutamento-e-selecao/medico-venha-trabalhar-conosco/medico-estrategia-saude-da-familia/"
ESPECIALIDADES_FILTER = [
    "Generalista",
    "Clínica Médica",
]


class Command(BaseCommand):
    help = "Clear tasks."

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS(
                "Iniciando scraping de vagas - Associação Saúde da Família"
            )
        )

        try:
            page = requests.get(f"{ASF_BASE_URL}{PAGE_URL}")
            soup = BeautifulSoup(page.text, "html.parser")
            tr_items = soup.find_all("tr")
            for tr in tr_items:
                td_items = tr.find_all("td")

                # UBS
                ubs = None
                if len(td_items) > 0:
                    internal_div = td_items[0].find("div")
                    if internal_div:
                        ubs = internal_div.string
                    else:
                        ubs = td_items[0].string

                # print(">>>>>>")
                # print("UBS: {}".format(ubs))

                # Endereço
                endereco_parts = []
                if len(td_items) > 1:
                    internal_links = td_items[1].find_all("a")
                    for link in internal_links:
                        if link.string:
                            endereco_parts.append(link.string.replace("\n", ""))
                        else:
                            for string in link.strings:
                                endereco_parts.append(string.replace("\n", ""))

                # Salários
                salarios = []
                if len(td_items) > 2:
                    for string in td_items[2].strings:
                        salario = string.replace("\n", "")
                        if salario and len(salario) > 0:
                            salarios.append(salario)

                # Benefício
                beneficios = []
                if len(td_items) > 3:
                    for string in td_items[3].strings:
                        beneficio = string.replace("\n", "")
                        if beneficio and len(beneficio) > 0:
                            beneficios.append(beneficio)

                # Carga horária
                cargas_horarias = []
                if len(td_items) > 4:
                    for string in td_items[4].strings:
                        carga = string.replace("\n", "")
                        if carga and len(carga) > 0:
                            cargas_horarias.append(carga)

                # Vagas / Especialidade
                especialidades = []
                if len(td_items) > 5:
                    especialidade_string = td_items[5].string
                    if especialidade_string:
                        especialidade = especialidade_string.replace("\n", "").replace(
                            "sem vagas", ""
                        )
                        if especialidade and len(especialidade) > 0:
                            especialidades.append(especialidade)
                    else:
                        for string in td_items[5].strings:
                            especialidade = string.replace("\n", "").replace(
                                "sem vagas", ""
                            )
                            if especialidade and len(especialidade) > 0:
                                especialidades.append(especialidade)

                if ubs and len(endereco_parts) > 0 and len(especialidades) > 0:
                    for especialidade in especialidades:
                        for filter in ESPECIALIDADES_FILTER:
                            if filter in especialidade:
                                print(">>>>>>")
                                print(f"UBS: {ubs}")
                                print("Endereço: {}".format(", ".join(endereco_parts)))
                                print(f"Salários: {salarios}")
                                print("Benefício: {}".format(" | ".join(beneficios)))
                                print(f"Carga horária: {cargas_horarias}")
                                print(f"Vagas / Especialidade: {especialidades}")

                                (
                                    created_vaga,
                                    created,
                                ) = Vaga.objects.update_or_create(
                                    ubs=ubs,
                                    endereco=", ".join(endereco_parts),
                                    carga_horaria=", ".join(cargas_horarias),
                                    salario_base=", ".join(salarios),
                                    beneficios=", ".join(" | ".join(beneficios)),
                                    especialidades=especialidade,
                                    fonte="Associação Saúde da Família",
                                )

        except Exception as e:
            print(e)
