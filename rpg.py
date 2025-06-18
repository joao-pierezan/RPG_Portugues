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

# --- Ajuste o tamanho das imagens dos bosses e do player ---
player_img = pygame.image.load("imagens/player.png")
player_img = pygame.transform.scale(player_img, (450, 450))  # tamanho maior

boss_imgs = [
    pygame.image.load("imagens/repetente.png"),
    pygame.image.load("imagens/celso_russomano.png"),
    pygame.image.load("imagens/boss3.png"),
]

boss_imgs[0] = pygame.transform.scale(boss_imgs[0], (400, 500))  # tamanho maior
boss_imgs[1] = pygame.transform.scale(boss_imgs[1], (600, 700))  # tamanho maior
boss_imgs[2] = pygame.transform.scale(boss_imgs[2], (600, 800))  # tamanho maior

# Imagens dos personagens
player_img = pygame.image.load("imagens/player.png")
player_img = pygame.transform.scale(player_img, (500, 500))  # novo tamanho desejado

boss_imgs = [
    pygame.image.load("imagens/repetente.png"),
    pygame.image.load("imagens/celso_russomano.png"),
    pygame.image.load("imagens/boss3.png"),
]

boss_imgs[0] = pygame.transform.scale(boss_imgs[0], (400, 500))
boss_imgs[1] = pygame.transform.scale(boss_imgs[1], (600, 700))
boss_imgs[2] = pygame.transform.scale(boss_imgs[2], (600, 800))  # novo tamanho desejado

boss_explain_texts = [" Maxuelison Kleber Whellingthon. Um estudante do 9 ano do ensino fundamental com apenas 13 anos; de febem . Tendo reprovado 15 vezes, diz que “já viu professor nascer e se aposentar”.  Devido a sua carreira notável em sua série, criou autoridade maior que a do próprio diretor em sala de aula. Carregando um baralho espanhol,um narguilé montado em sua mochila e um jack daniels Tennessee Whiskey 700ml, pode causar  o terror em qualquer um que ousar cruzar o seu caminho.",
                      "Celso muçulmano é um advogado que jamais diz algo simples. Suas frases são construídas com mais de 50 palavras, cheias de subordinações, inversões e adjetivos extravagantes — e ele nunca para para respirar. “Excelentíssimos presentes nesta augusta assembléia, venho, por meio desta humilde e respeitosa manifestação, pleitear a vossa compreensão acerca do que, in casu, se configura como a mais complexa das estruturas sintáticas compostas, a qual, por óbvio, exige análise detida e criteriosa.” Ele se move lentamente, e lança palavras tão complexas que podem paralisar o jogador só de ouvir.",
                      ]

folha_img = pygame.image.load("imagens/folha.png")
folha_img = pygame.transform.scale(folha_img, (300, 50))  # ajuste para o tamanho do botão

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
last_result = None  # "acertou" ou "errou"
last_attack_name = ""
last_attack_effect = ""


# Dados dos bosses
bosses = [
    {
        "name": "Repetente do Fundão",
        "hp": 100,
        "max_hp": 100,
        "description": "Maxuelison Kleber Whellingthon. Um estudante do 9 ano com 13 anos da FEBEM. Repetente 15 vezes, carrega baralho, narguilé e whiskey.",
        "attacks": [
            {"name": "Ataque Surpresa",  "effect": "Boss joga uma bolinha de papel com toda força no jogador de forma sorrateira", "special": None},
            {"name": "Fumaça Neblinosa",  "effect": "A fumaça do narguilé causa neblina na sala, impedindo o jogador de prever o ataque", "special": None},
            {"name": "JBL com Funk",  "effect": "O repetente puxa de sua mochila uma jbl com MC Oruam com volume estourado, deixando o jogador surdo.", "special": None},
            {"name": "Interrupção do Fundão", "effect": "Repetente grita 'Fessôra!, fala peixe, bola, gato bem rápido em inglês no meio do turno,fazendo o jogador se distrair'", "special": None}
        ],
        "player_attacks": [
            {"name": "Trauma CLT",  "effect": "ogador mostra uma carteira de trabalho, causando um susto imensurável no boss", "special": "extra_turn"},
            {"name": "Operação Silêncio Suspeito",  "effect": "O jogador chama a guarda municipal, que enquadra o Repetente e apreende sua cg 125 com escapamento fuelTech 450, extremamente barulhento, deixando o boss deprimido", "special": None},
            {"name": "Fumace Interrompida",  "effect": "O jogador apaga o carvão do narguilé do Repetente, causando ansiedade no repetente que não poderá alimentar o seu vício em nicotina até chegar em casa", "special": None}
        ]
    },
    {
        "name": "Advogado Rebuscado",
        "hp": 150,
        "max_hp": 150,
        "description": "Celso Muçulmano, advogado que nunca diz algo simples. Frases com 50+ palavras, subordinações e adjetivos extravagantes.",
        "attacks": [
            {"name": "Processo Surpresa", "effect": "-“É bom você medir esse seu tom pra falar comigo, por algum acaso você sabe quem você tá falando?”. O advogado processa o jogador por crime de injúria. ", "special": None},
            {"name": "Foi sem querer, querendo", "effect": "Advogado atropela o jogador com sua Porsche Cayenne", "special": None},
            {"name": "Citação Infinda", "effect": "Advogado recita trechos da constituição de 1998, causando exaustão no player.", "special": "half_attack"},
        ],
        "player_attacks": [
            {"name": "Defesa Indesejada",  "effect": "Jogador obriga o boss a ser advogado do léo lins", "special": "skip_turn"},
            {"name": "Desdoutorização",  "effect": "Jogador argumenta que só é doutor quem tem doutorado", "special": "conditional_half"},
            {"name": "Operação Lava Toga",  "effect": "Jogador acusa o advogado de subornar o Juiz, levando os dois para a cadeia", "special": None},
            {"name": "Caos no Tribunal da Internet", "effect": "Jogador coloca o monark pra discutir com o advogado sobre liberdade de expressão, causando angústia no boss", "special": None}
        ]
    },
    {
        "name": "Ivelã Pereira",
        "hp": 200,
        "max_hp": 200,
        "description": "Doutora em Linguística, professora do IFSC. Especialista em fazer alunos sofrerem com gramática.",
        "attacks": [
            {"name": "Tradução ou Morte", "effect": "Ivela pede para o jogador traduzir uma frase aleatória em inglês, que se desestabiliza", "special": None},
            {"name": "Sono Antipedagógico", "effect": "Ivela coloca um documentário longo e chato sobre indígenas da floresta amazônica, que faz o player adormecer.", "special": None},
            {"name": "Redação Criminal", "effect": "Ivela dá uma advertência no aluno por usar gírias na redação", "special": None},
            {"name": "Expulsão por Motivos Desconhecidos", "effect": "Ivelã da uma suspensão no aluno por algo extremamente horrível que não pode ser citado", "special": None},
            {"name": "Aula Cancelada (Mas o Dano Fica)", "effect": "Ivela começa uma greve, causando a parada dos estudos gramaticais", "special": None}
        ],
        "player_attacks": [
            {"name": "O Anti-Professor",
             "effect": "Jogador pode spawnar o Guilherme, que atrapalha a aula de Ivelã com comentários desnecessários como'O bullying já emagreceu muita gente' fazendo a professora se distrair",
             "special": "conditional_half"},
            {"name": "HMMMMMm cafézinho",  "effect": "Jogador vai fazer café no meio da aula da Ivelã, causando agonia extrema no boss.", "special": "heal_50"},
            {"name": "Lava Educação",  "effect": "Jogador se torna um político renomado e desvia verba da educação, atrasando o seu salário, causando desestabilidade na professora.", "special": None},
            {"name": "Aula dos Porquês",  "effect": " Jogador sobrecarrega Ivelã com perguntas extremamente óbvias sobre gramática, causando um burnout na professora.", "special": None},
            {"name": "Piadocas",  "effect": "Jogador responde 'Presunto' no lugar de presente na chamada da professora", "special": None},
            {"name": "Intervalo Comercial",  "effect": "Jogador spawna os candidatos eleitorais do gariba, fazendo com que 20 minutos da preciosa aula de ivelã sejam perdidas. ", "special": None}
        ]
    }
]
boss_attack_indices = [0 for _ in bosses]
player_attack_indices = [0 for _ in bosses]
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

    # Não desenha mais nenhum retângulo, só detecta hover/click
    if x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height:
        if pygame.mouse.get_pressed()[0]:
            clicked = True

    draw_text_with_paper(text, font_medium, BLACK, x + width//2, y + height//2, True)
    return clicked

noslen1 = pygame.image.load("imagens/noslen1.png")
foto = pygame.transform.scale(noslen1, (300,320))

def draw_button_with_image(text, x, y, width, height, image, hover_color):
    mouse_pos = pygame.mouse.get_pos()
    clicked = False

    # Desenha a imagem de fundo do botão
    screen.blit(image, (x, y))

    # Remova o efeito de hover:
    # if x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height:
    #     hover_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    #     hover_surface.fill((*hover_color, 80))  # 80 = transparência
    #     screen.blit(hover_surface, (x, y))
    #     if pygame.mouse.get_pressed()[0]:
    #         clicked = True

    # Apenas detecta clique, sem destaque
    if x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height:
        if pygame.mouse.get_pressed()[0]:
            clicked = True

    # Apenas desenhe o texto, sem papel extra
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
            return ("easy", 15)
        if draw_button("Médio (25 de dano)", start_x + button_width + spacing, y_buttons, button_width, button_height, YELLOW, (200, 200, 0)):
            return ("medium", 25)
        if draw_button("Difícil (40 de dano)", start_x + (button_width + spacing) * 2, y_buttons, button_width, button_height, RED, (255, 100, 100)):
            return ("hard", 40)

        # Botão de teste para passar de boss
        if draw_button("TESTE: PASSAR DE BOSS", WIDTH//2 - 150, y_buttons + button_height + 60, 300, 50, PURPLE, (128, 0, 128)):
            bosses[current_boss]["hp"] = 0
            return ("victory", 0)

    # --- Ataques do turno (meio da tela) ---
    # Descrição do ataque baseado no dado (centralizada e fonte maior)
    if attack_description:
        center_y = HEIGHT // 2
        # Cor do texto: preto para boss 0 e 2, branco para boss 1
        if current_boss in [0, 2]:
            desc_color = BLACK
        else:
            desc_color = WHITE
        draw_text(f"Resultado do dado: {dice_roll}", font_large, YELLOW, WIDTH//2, center_y - 30, True)
        draw_text(attack_description, font_large, desc_color, WIDTH//2, center_y + 20, True)
        y_offset += 60

    # --- Infos e lifebar na parte de baixo ---
    bottom_y = HEIGHT - 80

    # Desenha imagem do player acima da barra de vida
    screen.blit(player_img, (-80, bottom_y - player_img.get_height() - 30))

    # Jogador (esquerda)
    draw_text(f"João Carbonari", font_medium, WHITE, 10, bottom_y)
    draw_hp_bar(player_hp, 200, 10, bottom_y + 30, 350, 30, GREEN)
    draw_text(f"Vida: {player_hp}/200", font_small, WHITE, 80, bottom_y + 65)

    # --- POSIÇÕES INDIVIDUAIS DOS BOSSES ---
    boss_positions = [
        (WIDTH - 450, bottom_y - boss_imgs[0].get_height() - 50),  # Boss 0
        (WIDTH - 530, bottom_y - boss_imgs[1].get_height() - 50),  # Boss 1
        (WIDTH - 500, bottom_y - boss_imgs[2].get_height() - 50),  # Boss 2
    ]
    boss_x, boss_y = boss_positions[current_boss]
    screen.blit(boss_imgs[current_boss], (boss_x, boss_y))

    # Boss (direita)
    boss = bosses[current_boss]
    draw_text(f"{boss['name']}", font_medium, RED, WIDTH - 250, bottom_y)
    draw_hp_bar(boss["hp"], boss["max_hp"], WIDTH - 400, bottom_y + 30, 350, 30, RED)
    draw_text(f"Vida: {boss['hp']}/{boss['max_hp']}", font_small, WHITE, WIDTH - 320, bottom_y + 65)

    # Exibe o resultado do último ataque no centro da tela, se houver
    if last_result is not None:
        msg = "Você acertou!" if last_result == "acertou" else "Você errou!"
        color = GREEN if last_result == "acertou" else RED
        draw_text(msg, font_large, color, WIDTH//2, HEIGHT//2 - 60, True)
        draw_text(f"Ataque: {last_attack_name}", font_large, YELLOW, WIDTH//2, HEIGHT//2, True)
        # Fonte preta para boss 0 e 2, branca para boss 1
        efeito_cor = BLACK if current_boss in [0, 2] else WHITE
        draw_text(last_attack_effect, font_medium, efeito_cor, WIDTH//2, HEIGHT//2 + 50, True)

    return None

def draw_question_screen(question_data):
    screen.fill(BLACK)

    # Centraliza o bloco da pergunta
    question_box_width = 1000
    question_box_height = 120
    question_box_x = WIDTH//2 - question_box_width//2
    question_box_y = HEIGHT//2 - 220  # Ajuste vertical para centralizar tudo

    # Desenha a folha no fundo da questão
    folha_question = pygame.transform.scale(folha_img, (question_box_width, question_box_height))
    screen.blit(folha_question, (question_box_x, question_box_y))

    # Sempre mostra a pergunta normalmente
    draw_text(question_data["question"], font_medium, BLACK, WIDTH//2, question_box_y + question_box_height//2, True)

    # Centraliza as alternativas logo abaixo da pergunta
    option_width = 700
    option_height = 50
    option_x = WIDTH//2 - option_width//2

    num_options = len(question_data["options"])
    y_offset = question_box_y + question_box_height + 40  # 40px de espaço após a pergunta
    folha_alt = pygame.transform.scale(folha_img, (option_width, option_height))

    for i, option in enumerate(question_data["options"]):
        alt_y = y_offset + i * (option_height + 20)
        if draw_button(f"{chr(65 + i)}) {option}", option_x, alt_y, option_width, option_height, BLACK, BLACK):
            return i

    return None

def draw_intro_screen():
    screen.blit(intro_img, (0, 0))

    draw_text_with_paper("RPG Periodo Composto", font_title, BLACK, WIDTH//2, 120, True)

    # Botões
    button_width = 300
    button_height = 50
    spacing = 30
    num_buttons = 3
    total_height = num_buttons * button_height + (num_buttons - 1) * spacing
    start_y = HEIGHT // 2 - total_height // 2

    # INICIAR
    if draw_button_with_image("INICIAR", WIDTH//2 - button_width//2, start_y, button_width, button_height, folha_img, (0, 200, 0)):
        return "start"
    # CONFIGURAÇÕES (sem função)
    if draw_button_with_image("CONFIGURAÇÕES", WIDTH//2 - button_width//2, start_y + button_height + spacing, button_width, button_height, folha_img, (100, 100, 255)):
        pass
    # SAIR DO JOGO
    if draw_button_with_image("SAIR DO JOGO", WIDTH//2 - button_width//2, start_y + 2*(button_height + spacing), button_width, button_height, folha_img, (200, 0, 0)):
        pygame.quit()
        sys.exit()

    return None

def draw_victory_screen():
    screen.fill(BLACK)
    
    boss = bosses[current_boss]
    draw_text(f"VITÓRIA CONTRA {boss['name'].upper()}!", font_title, YELLOW, WIDTH//2, HEIGHT//2 - 120, True)
    
    if current_boss == 0:
        story = [
            "",
            "",
            "Você derrotou o Repetente do Fundão!",
            "Ele dropa uma Julieti que pode ser usada como item cosmético.",
            "Você adormece novamente, indo para a próxima batalha..."
        ]
    elif current_boss == 1:
        story = [
            "",
            "",
            "Você derrotou o Advogado Rebuscado!",
            "Ele dropa um maço de dinheiro que seria usado para subornar o juiz.",
            "Você toma uma rasteira de um guarda e apaga..."
        ]
    else:
        story = [
            "",
            "",
            "VOCÊ DERROTOU IVELÃ PEREIRA!",
            "Você cai de exaustão no chão, mas sabe que tudo valeu a pena.",
            "Sua alma foi recuperada e você passou de semestre!"
        ]
    
    # Centraliza o bloco de texto verticalmente
    total_lines = len(story)
    start_y = HEIGHT//2 - (total_lines * 30)
    for line in story:
        draw_text(line, font_medium, WHITE, WIDTH//2, start_y, True)
        start_y += 60

    # Botão centralizado
    if draw_button("CONTINUAR", WIDTH//2 - 100, HEIGHT//2 + 120, 200, 50, GREEN, (0, 200, 0)):
        return True
    
    return False

def draw_game_over_screen():
    screen.fill(BLACK)
    
    # Centraliza o título
    draw_text("GAME OVER", font_title, RED, WIDTH//2, 120, True)
    draw_text("Você não conseguiu derrotar todos os bosses...", font_medium, WHITE, WIDTH//2, 200, True)
    
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
    
    # Centraliza verticalmente o bloco de texto
    line_height = 40
    total_height = len(ending) * line_height
    y_offset = HEIGHT // 2 - total_height // 2

    for line in ending:
        draw_text(line, font_small, WHITE, WIDTH//2, y_offset, True)
        y_offset += line_height

    if draw_button("TENTAR NOVAMENTE", WIDTH//2 - 150, HEIGHT - 100, 300, 50, GREEN, (0, 200, 0)):
        reset_game()
        return True
    
    return False

def draw_ending_screen():
    screen.fill(BLACK)
    
    # Finais baseados na vida do jogador ao derrotar o boss final
    if player_hp >= 150:
        draw_text("FINAL BOM: YOUTUBER", font_title, GREEN, WIDTH//2, 100, True)
        ending_text = [
            "",
            "Você terminou com muita vida!",
            "",
            "Você vira youtuber de língua portuguesa falido,",
            "precisando se humilhar com gracinhas nos vídeos",
            "para entreter alunos com TDAH e criar engajamento."
        ]
        # Mostra a imagem só se ela foi carregada corretamente
        if noslen1.get_width() > 1:
            screen.blit(noslen1, (WIDTH - 700, 200))
    elif player_hp >= 75:
        draw_text("FINAL MEDIANO: PROFESSOR", font_title, YELLOW, WIDTH//2, 100, True)
        ending_text = [
            "",
            "Você terminou com vida razoável...",
            "",
            "Você vira professor de português do ensino médio",
            "mal remunerado em uma escola estadual",
            "no interior do Tocantins."
        ]
    else:
        draw_text("FINAL RUIM: CORRETOR ALHEIO", font_title, RED, WIDTH//2, 100, True)
        ending_text = [
            "",
            "Você terminou quase sem vida...",
            "",
            "Você passa a corrigir o português de posts no Twitter",
            "para se sentir brevemente superior e suprir seu vazio interno."
        ]
    
    # Centraliza verticalmente o bloco de texto
    line_height = 40
    total_height = len(ending_text) * line_height
    y_offset = HEIGHT // 2 - total_height // 2

    for line in ending_text:
        draw_text(line, font_medium, WHITE, WIDTH//2, y_offset, True)
        y_offset += line_height

    if draw_button("JOGAR NOVAMENTE", WIDTH//2 - 150, HEIGHT - 100, 300, 50, GREEN, (0, 200, 0)):
        reset_game()
        return True
    
    return False

def reset_game():
    global player_hp, current_boss, correct_answers, wrong_answers, game_state
    global boss_attack_indices, player_attack_indices
    player_hp = 200
    current_boss = 0
    correct_answers = 0
    wrong_answers = 0
    game_state = "intro"
    boss_attack_indices = [0 for _ in bosses]
    player_attack_indices = [0 for _ in bosses]
    # Reset boss HPs
    for boss in bosses:
        boss["hp"] = boss["max_hp"]

def boss_turn():
    global player_hp, boss_attacks_this_turn, boss_attack_indices

    boss = bosses[current_boss]
    boss_attacks_this_turn = []

    # Ataque em ordem, looping
    idx = boss_attack_indices[current_boss]
    attack = boss["attacks"][idx]
    boss_attack_indices[current_boss] = (idx + 1) % len(boss["attacks"])

    boss_attacks_this_turn.append(attack)

    # Verifica se o jogador morreu
    if player_hp <= 0:
        return "game_over"

    return attack["special"]

def show_result_screen(acertou, ataque, efeito):
    # Exibe o resultado (acerto/erro) e o ataque correspondente no centro da tela por 2 segundos
    screen.fill(BLACK)
    msg = "Você acertou!" if acertou else "Você errou!"
    draw_text(msg, font_large, GREEN if acertou else RED, WIDTH//2, HEIGHT//2 - 60, True)
    draw_text(f"Ataque: {ataque}", font_large, YELLOW, WIDTH//2, HEIGHT//2, True)
    draw_text(efeito, font_medium, WHITE, WIDTH//2, HEIGHT//2 + 50, True)
    pygame.display.flip()
    pygame.time.delay(2000)

def player_turn(difficulty, damage):
    global player_hp, correct_answers, wrong_answers, player_attacks_this_turn
    global last_result, last_attack_name, last_attack_effect

    player_attacks_this_turn = []
    last_result = None
    last_attack_name = ""
    last_attack_effect = ""

    # Escolhe uma pergunta baseada na dificuldade
    difficulty_level = 0 if difficulty == "easy" else 1 if difficulty == "medium" else 2
    question_data = random.choice(questions[difficulty_level])

    # Mostra a tela de pergunta
    answer = None
    while answer is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        answer = draw_question_screen(question_data)
        pygame.display.flip()

    if answer == question_data["answer"]:
        correct_answers += 1
        # Ataque do player em ordem, looping
        idx = player_attack_indices[current_boss]
        player_attack = bosses[current_boss]["player_attacks"][idx]
        player_attack_indices[current_boss] = (idx + 1) % len(bosses[current_boss]["player_attacks"])
        player_attacks_this_turn.append(player_attack)
        bosses[current_boss]["hp"] -= damage
        last_result = "acertou"
        last_attack_name = player_attack["name"]
        last_attack_effect = player_attack["effect"]
        if bosses[current_boss]["hp"] <= 0:
            return "victory"
        if player_attack.get("special") in ["extra_turn", "skip_turn"]:
            return player_attack["special"]
        return None
    else:
        wrong_answers += 1
        boss_attack = random.choice(bosses[current_boss]["attacks"])
        player_hp -= damage
        last_result = "errou"
        last_attack_name = boss_attack["name"]
        last_attack_effect = boss_attack["effect"]
        if player_hp <= 0:
            return "game_over"
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
        draw_text_with_paper(linha.strip(), font_medium, BLACK, WIDTH//2, y, True)
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
    textos_dos_bosses = ["Você acorda sem muito saber o que aconteceu, olha ao redor e percebe que está em uma sala de aula comum, você olha para o quadro e percebe que o conteúdo de substantivos está sendo passado, o que torna impossível reconhecer se você está na sexta série ou no terceirão. Pouco tempo se passa até que alguém entra pela porta, um homem visivelmente mais velho que todos os alunos daquela classe, ele imediatamente começa a lhe encarar, uma aura começa a crescer ao redor dele(igual a dos dragões heroicos do dragon city), você percebe que ele é o primeiro boss e a batalha começa.","Você acorda com as mãos atrás das costas e algemado, dois homens altos e uniformizados estão te acompanhando ao seu lado, você está no que parece ser uma casa chique e antiga, com decorações e entalhes de madeira envernizada na parede, você se pergunta aonde estão te levando, vocês param em frente a uma grande porta de madeira, que se abre sozinha, revelando um grande salão, você analisa o local por alguns segundos e percebe que está em um júri, e que o réu é você. Logo ao entrar você percebe alguém que se destaca em meio a todos os outros, um advogado, de terno e com cabelo alisado. Pouco depois esse homem aponta para você se e percebe que ele é o segundo boss. Uma aura (igual a de super sayajin) cresce ao redor dele e a segunda batalha começa.","Voce acorda novamente, desta vez em uma cadeira extremamente desconfortável, na sua frente uma mesa inclinada -“Quem foi o idiota que fez uma mesa inclinada?” você se pergunta. Olha ao seu redor e percebe que está totalmente sozinho em uma sala de aula do IFSC, com somente a sua carteira. Na sua frente, você vê um papel com o título “Recuperação de Portugues”. “O que está acontecendo?” Você se pergunta, mas antes mesmo de poder fazer hipóteses uma professora entra pela porta da sala, nada mais nada menos que Ivelã Pereira.Ivela para na sua frente e a batalha final começa."]
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
        draw_text_with_paper(linha.strip(), font_medium, BLACK, WIDTH//2, y, True)
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

def draw_boss_explain_screen(bossn):
    global mouse_released
    screen.blit(boss_bg_imgs[bossn], (0, 0))
    boss = bosses[bossn]
    desc = boss_explain_texts[bossn]

    # Quebra a descrição em linhas menores se necessário
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

    lines = wrap_text(desc, font_medium, 700)
    y = HEIGHT // 2 - (len(lines) * 20)

    # Desenha o texto à esquerda e a imagem do boss à direita (apenas para os 2 primeiros bosses)
    text_x = WIDTH // 2 - 200
    img_x = WIDTH // 2 + 300
    img_y = y - 40

    draw_text_with_paper(f"Boss: {boss['name']}", font_large, RED, text_x, y - 60, True)
    for line in lines:
        draw_text_with_paper(line.strip(), font_medium, BLACK, text_x, y, True)
        y += 40

    if bossn in [0, 1]:
        # Ajuste o tamanho da imagem se necessário
        boss_img = boss_imgs[bossn]
        screen.blit(boss_img, (img_x, img_y))

    # Botão para continuar
    clicked = draw_button("COMEÇAR BATALHA", WIDTH//2 - 150, HEIGHT - 100, 300, 50, GREEN, (0, 200, 0))

    # Controle de clique igual às outras telas
    if clicked:
        if mouse_released:
            mouse_released = False
            return True
    else:
        mouse_released = True
    return False

def draw_text_with_paper(text, font, color, x, y, centered=False, padding_x=40, padding_y=20):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y) if centered else (x, y))
    # Calcula o tamanho do papel com base no texto + padding
    paper_width = text_rect.width + padding_x * 2
    paper_height = text_rect.height + padding_y * 2
    paper_img = pygame.transform.scale(folha_img, (paper_width, paper_height))
    paper_rect = paper_img.get_rect(center=text_rect.center)
    screen.blit(paper_img, paper_rect)
    screen.blit(text_surface, text_rect)
    return text_rect

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
            last_result = None
            last_attack_name = ""
            last_attack_effect = ""
            game_state = "boss_explain"

    elif game_state == "boss_explain":
        # Só mostra a tela de descrição se NÃO for o último boss
        if current_boss < len(bosses) - 1:
            if draw_boss_explain_screen(current_boss):
                game_state = "battle"
        else:
            game_state = "battle"

    elif game_state == "battle":
        action = draw_battle_screen()
        if isinstance(action, tuple):
            difficulty, damage = action
            special_effect = player_turn(difficulty, damage)
            
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