"""Cria um usuário e uma família 100% fictícios para demonstração.

Uso:
    python manage.py seed_demo

Todos os nomes, datas, cidades e fotos são inventados. As fotos são
ilustrações geradas para o projeto (pessoas/static/pessoas/img/demo/).
"""
from datetime import date
from pathlib import Path

from django.contrib.auth.models import User
from django.core.files import File
from django.core.management.base import BaseCommand

from pessoas.models import Pessoa

DEMO_IMG_DIR = Path(__file__).resolve().parents[2] / "static" / "pessoas" / "img" / "demo"

FAMILIA = [
    # chave, nome, gênero, nascimento, falecimento, cidade, UF, foto, pai, mãe, cônjuge, história
    ("joaquim", "Joaquim Exemplo", "M", date(1938, 3, 12), date(2014, 8, 2), "Vila Aurora", "MG",
     "joaquim", None, None, None, "Marceneiro, construiu a primeira casa da família."),
    ("helena", "Helena Exemplo", "F", date(1942, 11, 5), None, "Campo Sereno", "MG",
     "helena", None, None, "joaquim", "Professora primária por mais de trinta anos."),
    ("carlos", "Carlos Exemplo", "M", date(1967, 6, 21), None, "Vila Aurora", "MG",
     "carlos", "joaquim", "helena", None, "Engenheiro agrônomo."),
    ("marta", "Marta Silvestre", "F", date(1970, 1, 30), None, "Lago Azul", "GO",
     "marta", None, None, "carlos", "Enfermeira e contadora de histórias."),
    ("lucas", "Lucas Exemplo", "M", date(1994, 9, 14), None, "Lago Azul", "GO",
     "lucas", "carlos", "marta", None, "Músico."),
    ("beatriz", "Beatriz Exemplo", "F", date(1997, 4, 3), None, "Lago Azul", "GO",
     "beatriz", "carlos", "marta", None, "Desenvolvedora de software."),
    ("rafael", "Rafael Fictício", "M", date(1995, 12, 18), None, "Serra Clara", "SP",
     "rafael", None, None, "beatriz", "Fotógrafo."),
    ("clara", "Clara Exemplo Fictício", "F", date(2021, 7, 9), None, "Serra Clara", "SP",
     "clara", "rafael", "beatriz", None, ""),
]


class Command(BaseCommand):
    help = "Cria o usuário 'demo' (senha 'demo12345') com uma árvore genealógica fictícia."

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(username="demo")
        user.set_password("demo12345")
        user.save()
        antigas = Pessoa.objects.filter(owner=user)
        for antiga in antigas:
            if antiga.foto:
                antiga.foto.delete(save=False)
        antigas.delete()

        pessoas = {}
        for (chave, nome, genero, nasc, falec, cidade, uf, foto,
             pai, mae, conjuge, historia) in FAMILIA:
            p = Pessoa(
                nome=nome, genero=genero, data_nascimento=nasc, data_falecimento=falec,
                local_nascimento=cidade, estado_nascimento=uf, owner=user,
                pai=pessoas.get(pai), mae=pessoas.get(mae),
                historia_pessoal=historia or None,
            )
            img = DEMO_IMG_DIR / f"{foto}.png"
            if img.exists():
                with img.open("rb") as fh:
                    p.foto.save(f"demo_{foto}.png", File(fh), save=False)
            p.save()
            pessoas[chave] = p
            if conjuge:
                outro = pessoas[conjuge]
                p.conjuge = outro
                p.save(update_fields=["conjuge"])
                outro.conjuge = p
                outro.save(update_fields=["conjuge"])

        self.stdout.write(self.style.SUCCESS(
            f"{len(pessoas)} pessoas fictícias criadas. Login: demo / demo12345"
        ))
