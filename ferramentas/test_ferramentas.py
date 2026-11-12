#!/usr/bin/env python3
"""Testes de verificar-coerencia.py e comparar-linha-base.py (só biblioteca padrão).

    python3 -m unittest discover -s ferramentas -v

Todo caso sintético nasce numa pasta temporária; nada é escrito no repositório.
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

AQUI = Path(__file__).resolve().parent
COERENCIA = AQUI / "verificar-coerencia.py"
LINHA_BASE = AQUI / "comparar-linha-base.py"


def sty(nome="pacote", data="2026/10/31", versao="0.5.3-alfa", corpo="\\relax\n"):
    return f"\\ProvidesPackage{{{nome}}}[{data} v{versao} Teste]\n{corpo}"


def rodar(*args):
    r = subprocess.run([sys.executable, "-I", *map(str, args)], capture_output=True, text=True)
    return r.returncode, r.stdout


class Coerencia(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.raiz = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def escrever(self, rel, texto):
        p = self.raiz / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(texto, encoding="utf-8")

    def verificar(self, *extra):
        return rodar(COERENCIA, "--raiz", self.raiz, *extra)

    def test_repositorio_coerente_passa(self):
        self.escrever("a/um.sty", sty("um"))
        self.escrever("b/dois.sty", sty("dois", corpo="\\relax\\relax\n"))
        rc, saida = self.verificar()
        self.assertEqual(rc, 0, saida)

    def test_mesmo_nome_corpos_diferentes_mesma_data_e_versao_falha(self):
        self.escrever("a/p.sty", sty(corpo="\\def\\a{1}\n"))
        self.escrever("b/p.sty", sty(corpo="\\def\\a{2}\n"))
        rc, saida = self.verificar()
        self.assertEqual(rc, 1, saida)
        self.assertIn("regra zero", saida)
        self.assertIn("compartilham data e versão", saida)

    def test_mesmo_nome_corpos_diferentes_datas_distintas_tambem_falha(self):
        self.escrever("a/p.sty", sty(corpo="\\def\\a{1}\n"))
        self.escrever("b/p.sty", sty(data="2026/11/12", versao="0.6.0-alfa", corpo="\\def\\a{2}\n"))
        rc, saida = self.verificar()
        self.assertEqual(rc, 1, saida)
        self.assertIn("nome declarado", saida)

    def test_mesmo_nome_mesmo_corpo_passa_apesar_da_declaracao(self):
        # a declaração é a parte que se reescreve ao arquivar: não conta
        self.escrever("a/p.sty", sty(corpo="\\def\\a{1}\n"))
        self.escrever("b/p.sty", sty(data="2026/09/04", versao="0.1.0", corpo="\\def\\a{1}\r\n"))
        rc, saida = self.verificar()
        self.assertEqual(rc, 0, saida)

    def test_declaracao_em_varias_linhas(self):
        self.escrever("a/c.cls", "\\ProvidesClass{c}[2026/07/03 v0.1\n  Descricao longa]\n\\relax\n")
        rc, saida = self.verificar()
        self.assertEqual(rc, 0, saida)

    def test_marcador_de_conflito_falha(self):
        self.escrever("a/p.sty", sty())
        self.escrever("a/nota.md", "texto\n<<<<<<< HEAD\nx\n=======\ny\n>>>>>>> outra\n")
        rc, saida = self.verificar()
        self.assertEqual(rc, 1, saida)
        self.assertIn("marcador de conflito", saida)

    def test_linha_de_sinais_de_igual_sozinha_nao_e_conflito(self):
        self.escrever("a/nota.md", "Titulo\n=======\n")
        rc, saida = self.verificar()
        self.assertEqual(rc, 0, saida)

    def test_changelog_com_versao_diferente_falha(self):
        self.escrever("crpsp-forms/formularios.sty", sty("formularios", "2026/09/04", "0.1.0-alfa"))
        self.escrever("crpsp-forms/CHANGELOG.md", "# x\n\n## 0.2.0-alfa — 2026/09/04\n")
        rc, saida = self.verificar()
        self.assertEqual(rc, 1, saida)
        self.assertIn("CHANGELOG", saida)

    def test_changelog_coerente_passa_e_data_diferente_so_avisa(self):
        self.escrever("crpsp-forms/formularios.sty", sty("formularios", "2026/09/04", "0.1.0-alfa"))
        self.escrever("crpsp-forms/CHANGELOG.md", "# x\n\n## 0.1.0-alfa — 2026-10-14\n")
        rc, saida = self.verificar()
        self.assertEqual(rc, 0, saida)
        self.assertIn("AVISO", saida)

    # --- --base: precisa de um repositório git de verdade ---------------------

    def git(self, *args):
        subprocess.run(
            ["git", "-C", str(self.raiz), "-c", "user.name=t", "-c", "user.email=t@t", *args],
            check=True, capture_output=True,
        )

    def repo_com_base(self, **kw):
        self.git("init", "-q")
        self.escrever("a/p.sty", sty(**kw))
        self.git("add", ".")
        self.git("commit", "-qm", "base")
        self.git("tag", "base")

    def test_base_corpo_mudou_sem_trocar_data_nem_versao_falha(self):
        self.repo_com_base(corpo="\\def\\a{1}\n")
        self.escrever("a/p.sty", sty(corpo="\\def\\a{2}\n"))
        rc, saida = self.verificar("--base", "base")
        self.assertEqual(rc, 1, saida)
        self.assertIn("a data continua", saida)
        self.assertIn("a versão continua", saida)

    def test_base_corpo_mudou_so_a_versao_falha(self):
        self.repo_com_base(corpo="\\def\\a{1}\n")
        self.escrever("a/p.sty", sty(versao="0.5.4-alfa", corpo="\\def\\a{2}\n"))
        rc, saida = self.verificar("--base", "base")
        self.assertEqual(rc, 1, saida)
        self.assertIn("a data continua", saida)

    def test_base_corpo_mudou_com_nova_data_e_versao_passa(self):
        self.repo_com_base(corpo="\\def\\a{1}\n")
        self.escrever("a/p.sty", sty("pacote", "2026/11/12", "0.6.0-alfa", "\\def\\a{2}\n"))
        rc, saida = self.verificar("--base", "base")
        self.assertEqual(rc, 0, saida)

    def test_base_so_a_declaracao_mudou_passa(self):
        self.repo_com_base(corpo="\\def\\a{1}\n")
        self.escrever("a/p.sty", sty(versao="0.5.3-beta", corpo="\\def\\a{1}\n"))
        rc, saida = self.verificar("--base", "base")
        self.assertEqual(rc, 0, saida)

    def test_base_versao_regrediu_falha(self):
        self.repo_com_base(corpo="\\def\\a{1}\n")
        self.escrever("a/p.sty", sty("pacote", "2026/11/12", "0.5.2-beta", "\\def\\a{2}\n"))
        rc, saida = self.verificar("--base", "base")
        self.assertEqual(rc, 1, saida)
        self.assertIn("regrediu", saida)

    def test_base_alfa_para_beta_do_mesmo_numero_nao_regride(self):
        self.repo_com_base(corpo="\\def\\a{1}\n")
        self.escrever("a/p.sty", sty("pacote", "2026/11/12", "0.5.3-beta", "\\def\\a{2}\n"))
        rc, saida = self.verificar("--base", "base")
        self.assertEqual(rc, 0, saida)

    def test_base_arquivo_novo_passa(self):
        self.repo_com_base()
        self.escrever("a/novo.sty", sty("novo"))
        rc, saida = self.verificar("--base", "base")
        self.assertEqual(rc, 0, saida)


class LinhaBase(unittest.TestCase):
    CAB = "arquivo\tmotor\tpaginas\tobjetos\terros_tagging\tfaltantes\tfatais\tprimeiro_erro\n"

    def comparar(self, rodada, base):
        with tempfile.TemporaryDirectory() as d:
            r, b = Path(d, "r.tsv"), Path(d, "b.tsv")
            r.write_text(self.CAB + rodada, encoding="utf-8")
            b.write_text(self.CAB + base, encoding="utf-8")
            return rodar(LINHA_BASE, r, b)

    def test_igual_passa_e_ignora_arquivo_nao_compilado(self):
        linha = "mwe/a.tex\tlualatex\t3\t18\t0\t0\t0\t\n"
        rc, saida = self.comparar(linha, linha + "mwe/b.tex\tlualatex\t1\t1\t0\t0\t0\t\n")
        self.assertEqual(rc, 0, saida)

    def test_pagina_diferente_falha(self):
        rc, saida = self.comparar(
            "mwe/a.tex\tlualatex\t4\t18\t0\t0\t0\t\n", "mwe/a.tex\tlualatex\t3\t18\t0\t0\t0\t\n"
        )
        self.assertEqual(rc, 1, saida)
        self.assertIn("paginas", saida)

    def test_erro_fatal_novo_falha(self):
        rc, saida = self.comparar(
            "mwe/a.tex\tlualatex\t-\t-\t0\t0\t3\t! Fatal\n", "mwe/a.tex\tlualatex\t3\t18\t0\t0\t0\t\n"
        )
        self.assertEqual(rc, 1, saida)

    def test_arquivo_fora_da_linha_base_falha(self):
        rc, saida = self.comparar("mwe/x.tex\tlualatex\t1\t1\t0\t0\t0\t\n", "mwe/a.tex\tlualatex\t1\t1\t0\t0\t0\t\n")
        self.assertEqual(rc, 1, saida)

    def test_rodada_vazia_falha(self):
        rc, saida = self.comparar("", "mwe/a.tex\tlualatex\t1\t1\t0\t0\t0\t\n")
        self.assertEqual(rc, 1, saida)


if __name__ == "__main__":
    unittest.main()
