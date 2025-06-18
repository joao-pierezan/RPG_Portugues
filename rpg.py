import pygame
import random
import sys
import time

# Inicialização do Pygame
pygame.init()
pygame.mixer.init()

# Configurações da tela
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RPG Periodo Composto")
# Carrega o som de fundo
#bg_music = pygame.mixer.Sound("imagens/som_fundo.ogg")
#bg_music.play(-1)

# Imagens de fundo
intro_img = pygame.image.load("imagens/fundo1.jpeg")
intro_img = pygame.transform.scale(intro_img, (WIDTH, HEIGHT))

boss_bg_imgs = [
    pygame.image.load("imagens/fundo2.jpeg"),
    pygame.image.load("imagens/fundo3.webp"),
    pygame.image.load("imagens/fundo4.jpg"),
]
for i in range(len(boss_bg_imgs)):
    boss_bg_imgs[i] = pygame.transform.scale(boss_bg_imgs[i], (WIDTH, HEIGHT))

# Imagens dos personagens
player_img = pygame.image.load("imagens/player.png")
player_img = pygame.transform.scale(player_img, (300, 300))  # novo tamanho desejado

boss_imgs = [
    pygame.image.load("imagens/repetente.png"),
    pygame.image.load("imagens/celso_russomano.png"),
    pygame.image.load("imagens/boss3.png"),
]

boss_imgs[0] = pygame.transform.scale(boss_imgs[0], (300, 320))
boss_imgs[1] = pygame.transform.scale(boss_imgs[1], (300, 320))
boss_imgs[2] = pygame.transform.scale(boss_imgs[2], (300, 400))  # novo tamanho desejado
# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
GRAY = (128, 128, 128)

# Fontes
font_small = pygame.font.SysFont("Arial", 16)
font_medium = pygame.font.SysFont("Arial", 24)
font_large = pygame.font.SysFont("Arial", 32)
font_title = pygame.font.SysFont("Arial", 48)

# Variáveis do jogo
player_hp = 200
current_boss = 0
correct_answers = 0
wrong_answers = 0
game_state = "intro"  # intro, context, battle, victory, game_over, ending
context_index = 0     # controla qual contexto mostrar
dice_roll = 1
attack_description = ""
boss_attacks_this_turn = []
player_attacks_this_turn = []
context_paragraph = 0
mouse_released = True

# Dados dos bosses
bosses = [
    {
        "name": "Repetente do Fundão",
        "hp": 100,
        "description": "Maxuelison Kleber Whellingthon. Um estudante do 9 ano com 13 anos da FEBEM. Repetente 15 vezes, carrega baralho, narguilé e whiskey.",
        "attacks": [
            {"name": "Ataque Surpresa", "damage": 15, "effect": "Joga bolinha de papel", "special": None},
            {"name": "Fumaça Neblinosa", "damage": 0, "effect": "Alternativas ilegíveis na próxima pergunta", "special": "no_alternatives"},
            {"name": "JBL com Funk", "damage": 0, "effect": "Não ouve a próxima pergunta", "special": "no_sound"},
            {"name": "Interrupção do Fundão", "damage": 10, "effect": "Distrai com perguntas aleatórias", "special": None}
        ],
        "player_attacks": [
            {"name": "Mostra Carteira de Trabalho", "damage": 0, "effect": "Boss perde o turno", "special": "extra_turn"},
            {"name": "Chama Guarda Municipal", "damage": 30, "effect": "Recupera 40 de vida", "special": "heal_40"},
            {"name": "Apaga Carvão do Narguilé", "damage": 30, "effect": "Causa ansiedade no boss", "special": None}
        ]
    },
    {
        "name": "Advogado Rebuscado",
        "hp": 150,
        "description": "Dr. Fran, advogado que nunca diz algo simples. Frases com 50+ palavras, subordinações e adjetivos extravagantes.",
        "attacks": [
            {"name": "Processo Surpresa", "damage": 10, "effect": "Processa por injúria", "special": None},
            {"name": "Foi sem querer, querendo", "damage": 25, "effect": "Atropela com BMW X5", "special": None},
            {"name": "Citação Infinda", "damage": 0, "effect": "Reduz seu ataque pela metade", "special": "half_attack"},
        ],
        "player_attacks": [
            {"name": "Obriga ser advogado do Léo Lins", "damage": 0, "effect": "Boss não ataca por 1 turno", "special": "skip_turn"},
            {"name": "Doutor só com doutorado", "damage": 0, "effect": "Ataque do boss reduzido se errar", "special": "conditional_half"},
            {"name": "Acusa de suborno", "damage": 0, "effect": "Recupera 30 de vida", "special": "heal_30"},
            {"name": "Coloca Monark pra discutir", "damage": 20, "effect": "Dano adicional", "special": None}
        ]
    },
    {
        "name": "Ivelã Pereira",
        "hp": 200,
        "description": "Doutora em Linguística, professora do IFSC. Especialista em fazer alunos sofrerem com gramática.",
        "attacks": [
            {"name": "Traduzir frase em inglês", "damage": 20, "effect": "Dano adicional", "special": None},
            {"name": "Documentário chato", "damage": 0, "effect": "Perde próximo turno", "special": "skip_turn"},
            {"name": "Advertência por gírias", "damage": 10, "effect": "Dano adicional", "special": None},
            {"name": "Suspensão", "damage": 999, "effect": "FIM DE JOGO", "special": "instant_kill"},
            {"name": "Greve", "damage": 0, "effect": "Sem alternativas na próxima", "special": "no_alternatives"}
        ],
        "player_attacks": [
            {"name": "Spawna Guilherme", "damage": 0, "effect": "Ataque do boss reduzido se errar", "special": "conditional_half"},
            {"name": "Faz café", "damage": 0, "effect": "Recupera 50 de vida", "special": "heal_50"},
            {"name": "Vira político", "damage": 10, "effect": "Dano adicional", "special": None},
            {"name": "Sobrecarrega com perguntas", "damage": 25, "effect": "Burnout na professora", "special": None},
            {"name": "Responde 'Presunto'", "damage": 15, "effect": "Confusão na chamada", "special": None},
            {"name": "Spawna candidatos do Gariba", "damage": 0, "effect": "Perde 20 minutos de aula", "special": "skip_if_wrong"}
        ]
    }
]

# Perguntas do jogo (período composto)
questions = [
    # Fácil damage 15
    [
        {"question": "O que é um período composto?", 
         "options": ["Uma frase com apenas um verbo", "Uma frase com dois ou mais verbos (orações)", "Uma frase sem sujeito", "Uma palavra isolada"], 
         "answer": 1, "damage": 15},
         
        {"question": "Qual das opções é um exemplo de período composto?", 
         "options": ["Eu estudei", "Choveu ontem", "Fui ao mercado e comprei frutas", "Amanhã viajarei"], 
         "answer": 2, "damage": 15},
         
        {"question": "'Cheguei em casa e liguei a TV.' Quantas orações há nesse período?", 
         "options": ["1", "2", "3", "4"], 
         "answer": 1, "damage": 15},
         
        {"question": "Qual conjunção pode ligar duas orações em um período composto?", 
         "options": ["mas", "porque", "e", "todas as anteriores"], 
         "answer": 3, "damage": 15},
         
        {"question": "'Fui ao mercado, porém estava fechado.' Qual a classificação da conjunção destacada?", 
         "options": ["Aditiva", "Adversativa", "Conclusiva", "Explicativa"], 
         "answer": 1, "damage": 15},
         
        {"question": "Qual desses períodos é composto?", 
         "options": ["Ela estudou muito", "Ele correu e caiu", "Choveu à noite", "Todos dormiram cedo"], 
         "answer": 1, "damage": 15},
         
        {"question": "O que é uma oração coordenada?", 
         "options": ["Uma oração que depende de outra", "Uma oração que tem sentido completo sozinha", "Uma oração sem verbo", "Uma oração que só existe em períodos simples"], 
         "answer": 1, "damage": 15},
         
        {"question": "'Fiquei em casa porque estava doente.' Qual a relação entre as orações?", 
         "options": ["Adição", "Oposição", "Causa", "Tempo"], 
         "answer": 2, "damage": 15},
         
        {"question": "Qual alternativa apresenta um período composto por coordenação?", 
         "options": ["Quando cheguei, ela já tinha saído", "Estudei bastante, mas não fui bem", "Se chover, cancelaremos o passeio", "Quero que você volte cedo"], 
         "answer": 1, "damage": 15},
         
        {"question": "'Se você sair, leve um guarda-chuva.' Qual é a oração principal?", 
         "options": ["Se você sair", "Leve um guarda-chuva", "As duas são principais", "Não há oração principal"], 
         "answer": 1, "damage": 15},
         
        {"question": "Qual é a função do 'que' em 'Espero que você venha'?", 
         "options": ["Pronome relativo", "Conjunção integrante", "Pronome interrogativo", "Advérbio"], 
         "answer": 1, "damage": 15},
         
        {"question": "'Ele disse que chegaria tarde.' Qual o tipo de oração subordinada?", 
         "options": ["Substantiva", "Adjetiva", "Adverbial", "Coordenada"], 
         "answer": 0, "damage": 15},
         
        {"question": "Qual alternativa contém uma oração subordinada adverbial temporal?", 
         "options": ["Falei com ela, embora estivesse ocupada", "Quando anoiteceu, acendemos as luzes", "O livro que comprei é ótimo", "Quero que você leia mais"], 
         "answer": 1, "damage": 15},
         
        {"question": "'O menino, que estava cansado, dormiu.' Qual a classificação da oração destacada?", 
         "options": ["Subordinada adjetiva restritiva", "Subordinada adjetiva explicativa", "Subordinada substantiva", "Coordenada sindética"], 
         "answer": 1, "damage": 15},
         
        {"question": "Qual é a conjunção que indica condição?", 
         "options": ["E", "Mas", "Se", "Porque"], 
         "answer": 2, "damage": 15}
    ],
    
    # Médio damage 25
    [
        {"question": "O que é um período composto?", 
         "options": ["Uma frase com apenas um verbo e uma ação", "Uma estrutura com duas ou mais orações, independentes ou dependentes", "Um texto longo com muitos parágrafos", "Uma oração sem sujeito"], 
         "answer": 1, "damage": 25},
         
        {"question": "Qual a principal diferença entre oração coordenada e oração subordinada?", 
         "options": ["Coordenadas são dependentes; subordinadas são independentes", "Coordenadas são ligadas por vírgulas; subordinadas por pronomes", "Coordenadas têm independência sintática; subordinadas dependem da principal", "Subordinadas sempre iniciam com conjunções"], 
         "answer": 2, "damage": 25},
         
        {"question": "O que caracteriza uma oração coordenada sindética?", 
         "options": ["Não possui conjunção", "É ligada por conjunção (ex: 'e', 'mas', 'ou')", "Sempre expressa causa", "Substitui um substantivo"], 
         "answer": 1, "damage": 25},
         
        {"question": "Dê um exemplo de período composto por coordenação.", 
         "options": ["Quando cheguei, ela dormia", "Ele estudou, mas não passou", "A casa que comprei é grande", "Porque choras?"], 
         "answer": 1, "damage": 25},
         
        {"question": "Dê um exemplo de período composto por subordinação.", 
         "options": ["Ela riu e ele sorriu", "Se você sair, leve um guarda-chuva", "O dia estava lindo, porém frio", "Todos cantaram e dançaram"], 
         "answer": 1, "damage": 25},
         
        {"question": "Identifique a conjunção e o tipo de relação em: 'Ele estudou bastante, mas não conseguiu passar.'", 
         "options": ["'mas' – conclusiva", "'mas' – adversativa", "'mas' – explicativa", "'mas' – condicional"], 
         "answer": 1, "damage": 25},
         
        {"question": "Transforme em período composto por coordenação: 'João chegou cedo. João foi embora tarde.'", 
         "options": ["João chegou cedo, foi embora tarde", "João chegou cedo e foi embora tarde", "João, que chegou cedo, foi embora tarde", "Chegando cedo, João foi embora tarde"], 
         "answer": 1, "damage": 25},
         
        {"question": "Em qual frase há uma oração subordinada?", 
         "options": ["Fui ao cinema e depois ao parque", "Acredito que ela virá amanhã", "Corri muito, mas cheguei atrasado", "Ele sorriu e acenou"], 
         "answer": 1, "damage": 25},
         
        {"question": "O que é uma oração subordinada adjetiva?", 
         "options": ["Uma oração que equivale a um adjetivo, introduzida por pronome relativo", "Uma oração que indica tempo", "Uma oração independente ligada por 'e'", "Uma oração que expressa dúvida"], 
         "answer": 0, "damage": 25},
         
        {"question": "Complete com uma oração subordinada adverbial de tempo: 'Assim que...'", 
         "options": ["Assim que chegar, me avise", "Assim que feliz, ela sorriu", "Assim que o livro, li rápido", "Assim que grande, o cachorro latiu"], 
         "answer": 0, "damage": 25},
         
        {"question": "Dê um exemplo de oração subordinada adverbial de causa.", 
         "options": ["Como estava doente, faltou ao trabalho", "Ele faltou, mas estava doente", "Quando doente, ele faltou", "Faltou porque quis"], 
         "answer": 0, "damage": 25},
         
        {"question": "Classifique a oração: 'Não fui porque estava doente.'", 
         "options": ["Coordenada adversativa", "Subordinada adverbial causal", "Subordinada substantiva", "Coordenada explicativa"], 
         "answer": 1, "damage": 25},
         
        {"question": "Qual o valor da conjunção 'mas' em: 'Estudei muito, mas tirei nota baixa.'?", 
         "options": ["Adição", "Causa", "Oposição/contraste", "Tempo"], 
         "answer": 2, "damage": 25},
         
        {"question": "Reescreva como período composto: 'Maria está cansada. Maria vai à escola mesmo assim.'", 
         "options": ["Maria está cansada, mas vai à escola", "Maria, cansada, vai à escola", "Maria vai à escola porque está cansada", "Cansada, Maria foi à escola"], 
         "answer": 0, "damage": 25},
         
        {"question": "O que é uma oração subordinada substantiva?", 
         "options": ["Uma oração que funciona como substantivo na frase", "Uma oração que modifica um adjetivo", "Uma oração ligada por 'e'", "Uma oração que indica lugar"], 
         "answer": 0, "damage": 25}
    ],
    
    # Difícil damage 40
    [
        {"question": "Analise sintaticamente o período: 'Se eu soubesse, teria te avisado.'", 
         "options": ["Oração principal: 'teria te avisado'; subordinada adverbial condicional: 'Se eu soubesse'", "Duas orações coordenadas sindéticas", "Oração principal: 'Se eu soubesse'; subordinada substantiva completiva nominal", "Período simples com verbo auxiliar"], 
         "answer": 0, "damage": 40},
         
        {"question": "Classifique as orações subordinadas na frase: 'Disse que viria, mas não veio.'", 
         "options": ["'que viria' - substantiva objetiva direta; 'mas não veio' - coordenada adversativa", "Ambas são orações subordinadas adverbiais", "'que viria' - adjetiva restritiva; 'mas não veio' - coordenada explicativa", "'que viria' - substantiva subjetiva; 'mas não veio' - subordinada concessiva"], 
         "answer": 0, "damage": 40},
         
        {"question": "Explique a diferença entre oração subordinada substantiva objetiva direta e objetiva indireta.", 
         "options": ["Objetiva direta completa verbo sem preposição; indireta exige preposição", "Direta modifica substantivo; indireta modifica verbo", "Ambas são introduzidas por pronomes relativos", "Direta é sempre iniciada por 'que'; indireta por 'se'"], 
         "answer": 0, "damage": 40},
         
        {"question": "Reescreva a frase substituindo a oração adjetiva por um adjunto adnominal: 'O aluno que estuda muito sempre tem bons resultados.'", 
         "options": ["O aluno estudioso sempre tem bons resultados", "O aluno, porque estuda muito, tem bons resultados", "O aluno estuda muito para ter bons resultados", "O aluno sempre tem bons resultados que estuda muito"], 
         "answer": 0, "damage": 40},
         
        {"question": "Classifique as orações no período: 'Embora tivesse pouco tempo, ele fez o trabalho que a professora pediu.'", 
         "options": ["'Embora tivesse pouco tempo' - subordinada adverbial concessiva; 'que a professora pediu' - subordinada adjetiva", "Ambas são orações coordenadas sindéticas", "'Embora tivesse pouco tempo' - subordinada substantiva; 'que a professora pediu' - coordenada explicativa", "'Embora tivesse pouco tempo' - subordinada adverbial temporal; 'que a professora pediu' - subordinada adverbial causal"], 
         "answer": 0, "damage": 40},
         
        {"question": "Identifique o tipo de oração subordinada adverbial: 'Ele saiu cedo para que chegasse a tempo.'", 
         "options": ["Concessiva", "Final", "Causal", "Temporal"], 
         "answer": 1, "damage": 40},
         
        {"question": "Transforme o período composto em simples: 'Como estava cansado, ele dormiu cedo.'", 
         "options": ["Ele dormiu cedo por estar cansado", "Ele estava cansado, então dormiu cedo", "Dormiu cedo porque estava cansado", "Cansado, mas dormiu cedo"], 
         "answer": 0, "damage": 40},
         
        {"question": "Identifique todas as orações do período: 'Assim que terminou o trabalho, foi embora sem se despedir.'", 
         "options": ["'Assim que terminou o trabalho' - subordinada adverbial temporal; 'foi embora sem se despedir' - principal", "Duas orações coordenadas explicativas", "'terminou o trabalho' - principal; 'foi embora' - subordinada substantiva", "Período simples com locução verbal"], 
         "answer": 0, "damage": 40},
         
        {"question": "Explique por que o período abaixo é um exemplo de subordinação: 'Espero que você compreenda a situação.'", 
         "options": ["Porque possui duas orações independentes ligadas por vírgula", "Porque 'que você compreenda a situação' depende sintaticamente do verbo 'espero'", "Porque as orações são coordenadas por conjunção adversativa", "Porque é um período simples com sujeito composto"], 
         "answer": 1, "damage": 40},
         
        {"question": "Classifique o tipo de oração: 'Mesmo que chova, iremos ao passeio.'", 
         "options": ["Subordinada adverbial condicional", "Subordinada adverbial concessiva", "Subordinada substantiva completiva", "Subordinada adjetiva restritiva"], 
         "answer": 1, "damage": 40},
         
        {"question": "Identifique o valor semântico da conjunção: 'Ele se esforçou tanto que passou no concurso.'", 
         "options": ["Consequência", "Causa", "Comparação", "Concessão"], 
         "answer": 0, "damage": 40},
         
        {"question": "Classifique as orações no período: 'Ele não só estudou como também fez exercícios.'", 
         "options": ["Coordenadas sindéticas aditivas", "Subordinadas adverbiais temporais", "Subordinadas substantivas predicativas", "Coordenadas assindéticas"], 
         "answer": 0, "damage": 40},
         
        {"question": "Reescreva trocando subordinação por coordenação: 'Porque estava doente, faltou à aula.'", 
         "options": ["Estava doente, portanto faltou à aula", "Como estava doente, então faltou à aula", "Faltou à aula porque estava doente", "Estava doente, mas faltou à aula"], 
         "answer": 0, "damage": 40},
         
        {"question": "Analise e classifique o período: 'Fique tranquilo, pois tudo dará certo.'", 
         "options": ["Período composto por coordenação (explicativa)", "Período composto por subordinação (causal)", "Período simples com aposto", "Período composto por subordinação (concessiva)"], 
         "answer": 0, "damage": 40},
         
        {"question": "Qual é o tipo de subordinação em: 'Embora não gostasse de falar em público, fez um ótimo discurso.'", 
         "options": ["Causal", "Concessiva", "Condicional", "Comparativa"], 
         "answer": 1, "damage": 40}
    ]
]

context_texts = [
    "Você é um aluno do instituto federal de santa catarina campus chapecó chamado João Henrique Carbonari Landenberg. Durante todo o semestre você ficou jogando valorant e comendo doritos na frente do pc ao invés de estudar, e por causa disso você acabou pegando pendência na matéria de portugues V.",
    "Desesperado, tenta buscar ajudas sobrenaturais. Com uma galinha angolana, um dicionário aurélio e uma redação do enem nota mil, você invoca o deus supremo da Gramática, o mesmo lhe oferece mudar a realidade e fazer você passar de semestre, porém com uma única condição, bobinha até, a SUA ALMA SERÁ DELE.",
    "Você aceita sem pensar duas vezes, mas se arrepende amargamente segundos depois. De joelhos você súplica ao deus supremo da gramática por sua alma. Mas ele que nasceu pobre mas não nasceu otário não ia devolver a sua alma e sair de mãos abanando.",
    "O deus lhe faz então uma proposta. Caso você derrote todos os bosses do período composto, ele iria devolver a sua alma mortal e ainda te passaria de semestre, e você, sem escolha alguma, aceita a proposta.",
    "Você adormece lentamente imaginando qual será o seu destino."
]

# Funções auxiliares
def roll_dice():
    return random.randint(1, 6)

def draw_text(text, font, color, x, y, centered=False):
    text_surface = font.render(text, True, color)
    if centered:
        text_rect = text_surface.get_rect(center=(x, y))
    else:
        text_rect = text_surface.get_rect(topleft=(x, y))
    screen.blit(text_surface, text_rect)
    return text_rect

def draw_button(text, x, y, width, height, color, hover_color):
    mouse_pos = pygame.mouse.get_pos()
    clicked = False
    
    if x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
        if pygame.mouse.get_pressed()[0]:
            clicked = True
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))
    
    draw_text(text, font_medium, BLACK, x + width//2, y + height//2, True)
    return clicked

def draw_hp_bar(current, max_hp, x, y, width, height, color):
    ratio = current / max_hp
    pygame.draw.rect(screen, GRAY, (x, y, width, height))
    pygame.draw.rect(screen, color, (x, y, width * ratio, height))

def draw_battle_screen():
    screen.blit(boss_bg_imgs[current_boss], (0, 0))

    # --- Botões de escolha de nível no topo ---
    if game_state == "battle":
        draw_text("Escolha o nível da pergunta:", font_medium, BLACK, WIDTH//2, 30, True)
        button_width = 200
        button_height = 40
        spacing = 40
        total_width = button_width * 3 + spacing * 2
        start_x = WIDTH//2 - total_width//2
        y_buttons = 70  # topo da tela

        if draw_button("Fácil (15 de dano)", start_x, y_buttons, button_width, button_height, BLUE, (100, 100, 255)):
            return "easy"
        if draw_button("Médio (25 de dano)", start_x + button_width + spacing, y_buttons, button_width, button_height, YELLOW, (200, 200, 0)):
            return "medium"
        if draw_button("Difícil (40 de dano)", start_x + (button_width + spacing) * 2, y_buttons, button_width, button_height, RED, (255, 100, 100)):
            return "hard"

    # --- Ataques do turno (meio da tela) ---
    y_offset = 150
    for attack in boss_attacks_this_turn:
        draw_text(f"{bosses[current_boss]['name']} usou {attack['name']}!", font_small, RED, 50, y_offset)
        draw_text(f"Efeito: {attack['effect']}", font_small, WHITE, 50, y_offset + 20)
        y_offset += 50

    for attack in player_attacks_this_turn:
        draw_text(f"Você usou {attack['name']}!", font_small, GREEN, 50, y_offset)
        draw_text(f"Efeito: {attack['effect']}", font_small, WHITE, 50, y_offset + 20)
        y_offset += 50

    # Descrição do ataque baseado no dado
    if attack_description:
        draw_text(f"Resultado do dado: {dice_roll}", font_medium, YELLOW, WIDTH//2, y_offset, True)
        draw_text(attack_description, font_small, WHITE, WIDTH//2, y_offset + 30, True)
        y_offset += 60

    # --- Infos e lifebar na parte de baixo ---
    bottom_y = HEIGHT - 80

    # Desenha imagem do player acima da barra de vida
    screen.blit(player_img, (-50, bottom_y - player_img.get_height() - 10))

    # Jogador (esquerda)
    draw_text(f"João Carbonari", font_medium, WHITE, 10, bottom_y)
    draw_hp_bar(player_hp, 200, 10, bottom_y + 30, 200, 20, GREEN)
    draw_text(f"Vida: {player_hp}/200", font_small, WHITE, 50, bottom_y + 55)

    # --- POSIÇÕES INDIVIDUAIS DOS BOSSES ---
    boss_positions = [
        (WIDTH - 280, bottom_y - boss_imgs[0].get_height() - 30),  # Boss 0
        (WIDTH - 280, bottom_y - boss_imgs[1].get_height() - 30),  # Boss 1
        (WIDTH - 260, bottom_y - boss_imgs[2].get_height() - 20),  # Boss 2
    ]
    boss_x, boss_y = boss_positions[current_boss]
    screen.blit(boss_imgs[current_boss], (boss_x, boss_y))

    # Boss (direita)
    boss = bosses[current_boss]
    draw_text(f"{boss['name']}", font_medium, RED, WIDTH - 250, bottom_y)
    draw_hp_bar(boss["hp"], bosses[current_boss]["hp"], WIDTH - 250, bottom_y + 30, 200, 20, RED)
    draw_text(f"Vida: {boss['hp']}/{bosses[current_boss]['hp']}", font_small, WHITE, WIDTH - 250, bottom_y + 55)

    return None

def draw_question_screen(question_data, no_alternatives=False, no_sound=False):
    screen.fill(BLACK)
    
    if no_sound:
        draw_text("Você não consegue ouvir a pergunta por causa do funk!", font_medium, RED, WIDTH//2, 100, True)
    else:
        draw_text(question_data["question"], font_medium, WHITE, WIDTH//2, 100, True)
    
    y_offset = 150
    if no_alternatives:
        draw_text("As alternativas estão ilegíveis por causa da fumaça!", font_medium, RED, WIDTH//2, y_offset, True)
        y_offset += 50
        
        # Mostra as opções como "A) ???", "B) ???", etc.
        for i in range(len(question_data["options"])):
            option_text = f"{chr(65 + i)}) ???"
            if draw_button(option_text, WIDTH//2 - 100, y_offset, 200, 40, PURPLE, (178, 102, 255)):
                return i
            y_offset += 50
    else:
        for i, option in enumerate(question_data["options"]):
            if draw_button(f"{chr(65 + i)}) {option}", WIDTH//2 - 200, y_offset, 400, 40, BLUE, (100, 100, 255)):
                return i
            y_offset += 50
    
    return None

def draw_intro_screen():
    screen.blit(intro_img, (0, 0))

    draw_text("RPG Periodo Composto", font_title, BLACK, WIDTH//2, 120, True)

    # Botões
    button_width = 300
    button_height = 50
    spacing = 30
    start_y = 250

    # INICIAR
    if draw_button("INICIAR", WIDTH//2 - button_width//2, start_y, button_width, button_height, BLACK, (0, 200, 0)):
        return "start"
    # CONFIGURAÇÕES (sem função)
    if draw_button("CONFIGURAÇÕES", WIDTH//2 - button_width//2, start_y + button_height + spacing, button_width, button_height, BLACK, (100, 100, 255)):
        pass
    # SAIR DO JOGO
    if draw_button("SAIR DO JOGO", WIDTH//2 - button_width//2, start_y + 2*(button_height + spacing), button_width, button_height, BLACK, (200, 0, 0)):
        pygame.quit()
        sys.exit()

    return None

def draw_victory_screen():
    screen.fill(BLACK)
    
    boss = bosses[current_boss]
    draw_text(f"VITÓRIA CONTRA {boss['name'].upper()}!", font_title, YELLOW, WIDTH//2, 100, True)
    
    if current_boss == 0:
        story = [
            "Você derrotou o Repetente do Fundão!",
            "Ele dropa uma Julieti que pode ser usada como item cosmético.",
            "Você adormece novamente, indo para a próxima batalha..."
        ]
    elif current_boss == 1:
        story = [
            "Você derrotou o Advogado Rebuscado!",
            "Ele dropa um maço de dinheiro que seria usado para subornar o juiz.",
            "Você toma uma rasteira de um guarda e apaga..."
        ]
    else:
        story = [
            "VOCÊ DERROTOU IVELÃ PEREIRA!",
            "Você cai de exaustão no chão, mas sabe que tudo valeu a pena.",
            "Sua alma foi recuperada e você passou de semestre!"
        ]
    
    y_offset = 180
    for line in story:
        draw_text(line, font_medium, WHITE, WIDTH//2, y_offset, True)
        y_offset += 40
    
    if draw_button("CONTINUAR", WIDTH//2 - 100, HEIGHT - 100, 200, 50, GREEN, (0, 200, 0)):
        return True
    
    return False

def draw_game_over_screen():
    screen.fill(BLACK)
    
    draw_text("GAME OVER", font_title, RED, WIDTH//2, 100, True)
    draw_text("Você não conseguiu derrotar todos os bosses...", font_medium, WHITE, WIDTH//2, 180, True)
    
    if wrong_answers >= 3:
        ending = [
            "FINAL PÉSSIMO: ALMA PERDIDA",
            "",
            "Você não recuperou sua alma e agora é obrigado",
            "a escrever a palavra 'pneumoultramicroscopicossilicovulcanoconiótico'",
            "sem parar num caderninho por toda a eternidade."
        ]
    else:
        ending = [
            "FINAL RUIM: CORRETOR ALHEIO",
            "",
            "Você passa a corrigir o português de posts no Twitter",
            "para se sentir brevemente superior e suprir seu vazio interno."
        ]
    
    y_offset = 240
    for line in ending:
        draw_text(line, font_small, WHITE, WIDTH//2, y_offset, True)
        y_offset += 30
    
    if draw_button("TENTAR NOVAMENTE", WIDTH//2 - 150, HEIGHT - 100, 300, 50, GREEN, (0, 200, 0)):
        reset_game()
        return True
    
    return False

def draw_ending_screen():
    screen.fill(BLACK)
    
    if wrong_answers == 0:
        draw_text("FINAL BOM: YOUTUBER", font_title, GREEN, WIDTH//2, 100, True)
        ending_text = [
            "Você não errou nenhuma pergunta!",
            "",
            "Você vira youtuber de língua portuguesa falido,",
            "precisando se humilhar com gracinhas nos vídeos",
            "para entreter alunos com TDAH e criar engajamento."
        ]
    elif wrong_answers <= 3:
        draw_text("FINAL MEDIANO: PROFESSOR", font_title, YELLOW, WIDTH//2, 100, True)
        ending_text = [
            "Você errou algumas perguntas...",
            "",
            "Você vira professor de português do ensino médio",
            "mal remunerado em uma escola estadual",
            "no interior do Tocantins."
        ]
    else:
        draw_text("FINAL RUIM: CORRETOR ALHEIO", font_title, RED, WIDTH//2, 100, True)
        ending_text = [
            "Você errou muitas perguntas...",
            "",
            "Você passa a corrigir o português de posts no Twitter",
            "para se sentir brevemente superior e suprir seu vazio interno."
        ]
    
    y_offset = 180
    for line in ending_text:
        draw_text(line, font_medium, WHITE, WIDTH//2, y_offset, True)
        y_offset += 40
    
    if draw_button("JOGAR NOVAMENTE", WIDTH//2 - 150, HEIGHT - 100, 300, 50, GREEN, (0, 200, 0)):
        reset_game()
        return True
    
    return False

def reset_game():
    global player_hp, current_boss, correct_answers, wrong_answers, game_state
    player_hp = 200
    current_boss = 0
    correct_answers = 0
    wrong_answers = 0
    game_state = "intro"
    
    # Reset boss HPs
    for boss in bosses:
        boss["hp"] = bosses[bosses.index(boss)]["hp"]

def boss_turn():
    global player_hp, boss_attacks_this_turn
    
    boss = bosses[current_boss]
    boss_attacks_this_turn = []
    
    # Escolhe um ataque aleatório
    attack = random.choice(boss["attacks"])
    
    # Verifica se é o ataque mortal da Ivelã (1 em 6 chance)
    if current_boss == 2 and attack["name"] == "Suspensão" and random.randint(1, 6) != 1:
        # Escolhe outro ataque se não for o 1
        other_attacks = [a for a in boss["attacks"] if a["name"] != "Suspensão"]
        attack = random.choice(other_attacks)
    
    boss_attacks_this_turn.append(attack)
    
    # Aplica o dano
    if attack["damage"] > 0:
        player_hp -= attack["damage"]
    
    # Verifica se o jogador morreu
    if player_hp <= 0:
        return "game_over"
    
    return attack["special"]

def player_turn(difficulty):
    global player_hp, correct_answers, wrong_answers, dice_roll, attack_description, player_attacks_this_turn
    
    # Limpa ataques do turno anterior
    player_attacks_this_turn = []
    
    # Escolhe uma pergunta baseada na dificuldade
    difficulty_level = 0 if difficulty == "easy" else 1 if difficulty == "medium" else 2
    question_data = random.choice(questions[difficulty_level])
    
    # Mostra a tela de pergunta
    no_alternatives = any(attack.get("special") == "no_alternatives" for attack in boss_attacks_this_turn)
    no_sound = any(attack.get("special") == "no_sound" for attack in boss_attacks_this_turn)
    
    answer = None
    while answer is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        answer = draw_question_screen(question_data, no_alternatives, no_sound)
        pygame.display.flip()
    
    # Rola o dado
    dice_roll = roll_dice()
    
    # Determina a descrição do ataque baseado no dado
    attack_descriptions = [
        "Você ataca com um lápis afiado!",
        "Você usa o dicionário Aurélio como arma!",
        "Você lança uma borracha na cabeça do inimigo!",
        "Você argumenta com lógica gramatical!",
        "Você cita Machado de Assis para confundir o inimigo!",
        "Você usa a redação nota mil como escudo e ataca!"
    ]
    attack_description = attack_descriptions[dice_roll - 1]
    
    # Verifica se a resposta está correta
    if answer == question_data["answer"]:
        correct_answers += 1
        
        # Escolhe um ataque aleatório do jogador contra este boss
        player_attack = random.choice(bosses[current_boss]["player_attacks"])
        player_attacks_this_turn.append(player_attack)
        
        # Aplica o dano
        bosses[current_boss]["hp"] -= question_data["damage"] + (dice_roll * 2)
        
        # Aplica efeitos especiais
        if player_attack["damage"] > 0:
            bosses[current_boss]["hp"] -= player_attack["damage"]
        
        if player_attack.get("special") == "heal_40":
            player_hp = min(200, player_hp + 40)
        elif player_attack.get("special") == "heal_30":
            player_hp = min(200, player_hp + 30)
        elif player_attack.get("special") == "heal_50":
            player_hp = min(200, player_hp + 50)
        
        # Verifica se o boss morreu
        if bosses[current_boss]["hp"] <= 0:
            return "victory"
        
        # Efeitos que afetam o próximo turno
        if player_attack.get("special") in ["extra_turn", "skip_turn"]:
            return player_attack["special"]
        
        return None
    else:
        wrong_answers += 1
        
        # O boss contra-ataca com o mesmo dano
        bosses[current_boss]["hp"] -= question_data["damage"] // 2  # Dano reduzido por errar
        player_hp -= question_data["damage"]
        
        # Verifica se o jogador morreu
        if player_hp <= 0:
            return "game_over"
        
        # Verifica efeitos condicionais
        if any(attack.get("special") == "conditional_half" for attack in player_attacks_this_turn):
            return "boss_half_attack"
        
        if any(attack.get("special") == "skip_if_wrong" for attack in player_attacks_this_turn) and random.choice([True, False]):
            return "skip_turn"
        
        return None

def draw_context_screen():
    global mouse_released
    screen.blit(intro_img, (0, 0))
    texto = context_texts[context_paragraph]

    # Quebra o texto em várias linhas se for muito longo
    def wrap_text(text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] > max_width:
                lines.append(current_line)
                current_line = word + " "
            else:
                current_line = test_line
        lines.append(current_line)
        return lines

    linhas = wrap_text(texto, font_medium, 700)  # 700 é a largura máxima da caixa de texto

    y = HEIGHT // 2 - (len(linhas) * 20)
    for linha in linhas:
        draw_text(linha.strip(), font_medium, BLACK, WIDTH//2, y, True)
        y += 40

    # O botão é sempre desenhado
    clicked = draw_button("CONTINUAR", WIDTH//2 - 100, HEIGHT - 100, 200, 50, GREEN, (0, 200, 0))

    # Só avança se o mouse foi solto e depois pressionado novamente
    if clicked:
        if mouse_released:
            mouse_released = False
            return True
    else:
        mouse_released = True
    return False

def draw_context_boss(bossn):
    global mouse_released
    screen.blit(boss_bg_imgs[bossn], (0, 0))
    textos_dos_bosses = ["Você acorda sem muito saber o que aconteceu, olha ao redor e percebe que está em uma sala de aula comum, você olha para o quadro e percebe que o conteúdo de substantivos está sendo passado, o que torna impossível reconhecer se você está na sexta série ou no terceirão. Pouco tempo se passa até que alguém entra pela porta, um homem visivelmente mais velho que todos os alunos daquela classe, ele imediatamente começa a lhe encarar, uma aura começa a crescer ao redor dele(igual a dos dragões heroicos do dragon city), você percebe que ele é o primeiro boss e a batalha começa.","Você acorda com as mãos atrás das costas e algemado, dois homens altos e uniformizados estão te acompanhando ao seu lado, você está no que parece ser uma casa chique e antiga, com decorações e entalhes de madeira envernizada na parede, você se pergunta aonde estão te levando, vocês param em frente a uma grande porta de madeira, que se abre sozinha, revelando um grande salão, você analisa o local por alguns segundos e percebe que está em um júri, e que o réu é você. Logo ao entrar você percebe alguém que se destaca em meio a todos, um advogado, de terno e com cabelo alisado. Pouco depois esse homem aponta para você se e percebe que ele é o segundo boss. Uma aura (igual a de super sayajin) cresce ao redor dele e a segunda batalha começa.","Voce acorda novamente, desta vez em uma cadeira extremamente desconfortável, na sua frente uma mesa inclinada -“Quem foi o idiota que fez uma mesa inclinada?” você se pergunta. Olha ao seu redor e percebe que está totalmente sozinho em uma sala de aula do IFSC, com somente a sua carteira. Na sua frente, você vê um papel com o título “Recuperação de Portugues”. “O que está acontecendo?” Você se pergunta, mas antes mesmo de poder fazer hipóteses uma professora entra pela porta da sala, nada mais nada menos que Ivelã Pereira.Ivela para na sua frente e uma aura igual a de Michael Jordan cresce ao redor dela, a batalha final começa."]
    texto = textos_dos_bosses[bossn]

    # Quebra o texto em várias linhas se for muito longo
    def wrap_text(text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] > max_width:
                lines.append(current_line)
                current_line = word + " "
            else:
                current_line = test_line
        lines.append(current_line)
        return lines

    linhas = wrap_text(texto, font_medium, 700)  # 700 é a largura máxima da caixa de texto

    y = HEIGHT // 2 - (len(linhas) * 20)
    for linha in linhas:
        draw_text(linha.strip(), font_medium, BLACK, WIDTH//2, y, True)
        y += 40

    # O botão é sempre desenhado
    clicked = draw_button("CONTINUAR", WIDTH//2 - 100, HEIGHT - 100, 200, 50, GREEN, (0, 200, 0))

    # Só avança se o mouse foi solto e depois pressionado novamente
    if clicked:
        if mouse_released:
            mouse_released = False
            return True
    else:
        mouse_released = True
    return False

# Loop principal do jogo
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(BLACK)
    
    if game_state == "intro":
        result = draw_intro_screen()
        if result == "start":
            game_state = "context"  # Troque para "context" aqui

    elif game_state == "context":
        if draw_context_screen():
            context_paragraph += 1
            if context_paragraph >= len(context_texts):
                context_paragraph = 0
                game_state = "boss_context"

    elif game_state == "boss_context":
        if draw_context_boss(current_boss):
            game_state = "battle"

    
    elif game_state == "battle":
        action = draw_battle_screen()
        
        if action in ["easy", "medium", "hard"]:
            special_effect = player_turn(action)
            
            if special_effect == "victory":
                game_state = "victory"
            elif special_effect == "game_over":
                game_state = "game_over"
            else:
                # Se não foi vitória ou derrota, é turno do boss
                if special_effect not in ["extra_turn", "skip_turn"]:
                    boss_special = boss_turn()
                    
                    if boss_special == "instant_kill":
                        game_state = "game_over"
                    elif boss_special == "game_over":
                        game_state = "game_over"
    
    elif game_state == "victory":
        if draw_victory_screen():
            if current_boss < len(bosses) - 1:
                current_boss += 1
                context_paragraph = 0  # Reinicia o contexto para o próximo boss
                game_state = "boss_context"
                boss_attacks_this_turn = []
                player_attacks_this_turn = []
                attack_description = ""
            else:
                game_state = "ending"
    
    elif game_state == "game_over":
        if draw_game_over_screen():
            game_state = "intro"
    
    elif game_state == "ending":
        if draw_ending_screen():
            game_state = "intro"
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()