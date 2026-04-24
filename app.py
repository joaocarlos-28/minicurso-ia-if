MEDIA_APROVACAO    = 7.0
MEDIA_RECUPERACAO  = 5.0
QTD_NOTAS          = 4          # número fixo de notas
 
LINHA  = "=" * 50
LINHA2 = "-" * 50
 
 
def cabecalho():
    print("\n" + LINHA)
    print("   🎓  CALCULADORA DE NOTAS - IF")
    print(LINHA)
 
 
def ler_float(mensagem: str, minimo: float = 0.0, maximo: float = 10.0) -> float:
    """
    Lê um número float do terminal com validação completa:
      - Aceita vírgula OU ponto como separador decimal (ex.: 7,5 ou 7.5)
      - Rejeita múltiplos separadores (ex.: 7.5.3 ou 7,5,3)
      - Rejeita letras ou caracteres especiais
      - Garante que o valor esteja entre minimo e maximo
    """
    while True:
        entrada = input(mensagem).strip()
 
        # Substitui vírgula por ponto para aceitar notação brasileira
        entrada_normalizada = entrada.replace(",", ".")
 
        # Rejeita se tiver mais de um ponto após a substituição
        if entrada_normalizada.count(".") > 1:
            print("  ⚠️  Formato inválido! Use apenas um separador decimal (ex.: 7,5 ou 7.5).\n")
            continue
 
        # Rejeita se estiver vazio
        if entrada_normalizada == "":
            print("  ⚠️  Campo obrigatório! Digite um número (ex.: 7,5).\n")
            continue
 
        try:
            valor = float(entrada_normalizada)
            if minimo <= valor <= maximo:
                return round(valor, 2)   # arredonda para 2 casas decimais
            else:
                print(f"  ⚠️  Valor fora do intervalo! Digite entre {minimo} e {maximo}.\n")
        except ValueError:
            print("  ⚠️  Entrada inválida! Digite apenas números (ex.: 7,5 ou 7.5).\n")
 
 
 
def barra_progresso(valor: float, maximo: float = 10.0, largura: int = 20) -> str:
    """Gera uma barra de progresso visual em texto."""
    preenchido = int((valor / maximo) * largura)
    vazio      = largura - preenchido
    return f"[{'█' * preenchido}{'░' * vazio}] {valor:.1f}"
 
 
def classificar(media: float) -> dict:
    """Retorna situação, símbolo e mensagem de incentivo."""
    if media >= MEDIA_APROVACAO:
        return {
            "situacao": "APROVADO",
            "simbolo":  "✅",
            "msg": "Parabéns! Excelente desempenho. Continue assim!",
        }
    elif media >= MEDIA_RECUPERACAO:
        faltam = MEDIA_APROVACAO - media
        return {
            "situacao": "RECUPERAÇÃO",
            "simbolo":  "⚠️ ",
            "msg": f"Atenção! Faltam {faltam:.2f} pontos para aprovação. Você ainda consegue!",
        }
    else:
        return {
            "situacao": "REPROVADO",
            "simbolo":  "❌",
            "msg": "Não desanime! Converse com seu professor e busque apoio.",
        }
 
 
def exibir_resultado(nome: str, notas: list[float]):
    """Exibe o resultado completo do aluno."""
    media = sum(notas) / len(notas)
    info  = classificar(media)
 
    print("\n" + LINHA)
    print(f"  📋  RESULTADO — {nome.upper()}")
    print(LINHA)
 
    # Notas individuais com barra
    print("\n  Notas lançadas:")
    for i, n in enumerate(notas, 1):
        print(f"    Nota {i}: {barra_progresso(n)}")
 
    print(LINHA2)
 
    # Estatísticas
    print(f"  Soma total : {sum(notas):.2f}")
    print(f"  Maior nota : {max(notas):.1f}")
    print(f"  Menor nota : {min(notas):.1f}")
    print(LINHA2)
 
    # Média e situação
    print(f"  Média Final: {media:.2f}  {barra_progresso(media)}")
    print(f"\n  Situação   : {info['simbolo']}  {info['situacao']}")
    print(f"\n  💡 {info['msg']}")
    print(LINHA)
 
 
def exibir_historico(historico: list[dict]):
    """Exibe a tabela de histórico de todos os alunos."""
    if not historico:
        print("\n  (Nenhum cálculo realizado ainda.)")
        return
 
    print("\n" + LINHA)
    print("  📜  HISTÓRICO DE CÁLCULOS")
    print(LINHA)
    print(f"  {'ALUNO':<20} {'MÉDIA':>6}  {'SITUAÇÃO'}")
    print(LINHA2)
    for h in historico:
        print(f"  {h['nome']:<20} {h['media']:>6.2f}  {h['simbolo']} {h['situacao']}")
    print(LINHA)
 
 
def menu_principal() -> str:
    """Exibe o menu e retorna a opção escolhida."""
    print("\n  O que deseja fazer?")
    print("  [1] Calcular média de um aluno")
    print("  [2] Ver histórico")
    print("  [0] Sair")
    return input("\n  Opção: ").strip()
 
 
# ── Programa principal ──────────────────────────────────────────────────────
def main():
    historico: list[dict] = []
 
    cabecalho()
 
    while True:
        opcao = menu_principal()
 
        # ── Calcular média ──────────────────────────────────────────────────
        if opcao == "1":
            print("\n" + LINHA2)
 
            # Nome do aluno
            nome = input("  Nome do aluno (ou ENTER para 'Aluno'): ").strip()
            if not nome:
                nome = "Aluno"
 
            # Leitura das 4 notas
            print(f"\n  Insira as {QTD_NOTAS} notas do aluno:\n")
            notas = []
            for i in range(1, QTD_NOTAS + 1):
                n = ler_float(f"  Digite a Nota {i} (0 a 10): ")
                notas.append(n)
 
            # Resultado
            exibir_resultado(nome, notas)
 
            # Salvar no histórico
            media = sum(notas) / len(notas)
            info  = classificar(media)
            historico.append({
                "nome":     nome,
                "media":    media,
                "situacao": info["situacao"],
                "simbolo":  info["simbolo"],
            })
 
        # ── Histórico ───────────────────────────────────────────────────────
        elif opcao == "2":
            exibir_historico(historico)
 
        # ── Sair ────────────────────────────────────────────────────────────
        elif opcao == "0":
            print("\n  Até logo! 👋\n")
            break
 
        else:
            print("\n  ⚠️  Opção inválida. Tente novamente.")
 
 
if __name__ == "__main__":
    main()
