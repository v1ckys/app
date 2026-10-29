import customtkinter as ctk
import sqlite3
import hashlib
from datetime import date, datetime
from tkinter import messagebox, simpledialog

DB_ARCHIVO = "fanframe.db"

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

COLOR_FONDO = "#FFF9FD"
COLOR_LILA = "#A77BC8"
COLOR_LILA_HOVER = "#8E6BB3"
COLOR_ROSA = "#C17FA0"
COLOR_ROSA_HOVER = "#A96386"
COLOR_TEXTO = "#453B50"
COLOR_TARJETA = "#F4EAFB"
COLOR_CELESTE = "#DCEFFA"

CATALOGO = [
    {"titulo": "Barbie", "categoria": "Película"},
    {"titulo": "Intensamente 2", "categoria": "Película"},
    {"titulo": "Spider-Man: No Way Home", "categoria": "Película"},
    {"titulo": "Orgullo y prejuicio", "categoria": "Película"},
    {"titulo": "10 cosas que odio de ti", "categoria": "Película"},
    {"titulo": "La La Land", "categoria": "Película"},
    {"titulo": "El viaje de Chihiro", "categoria": "Película"},
    {"titulo": "Titanic", "categoria": "Película"},
    {"titulo": "Stranger Things", "categoria": "Serie"},
    {"titulo": "Merlina", "categoria": "Serie"},
    {"titulo": "El verano en que me enamoré", "categoria": "Serie"},
    {"titulo": "Heartstopper", "categoria": "Serie"},
    {"titulo": "The Office", "categoria": "Serie"},
    {"titulo": "The Last of Us", "categoria": "Serie"},
    {"titulo": "Gilmore Girls", "categoria": "Serie"},
    {"titulo": "Friends", "categoria": "Serie"},
    {"titulo": "Cruel Summer", "categoria": "Canción"},
    {"titulo": "Espresso", "categoria": "Canción"},
    {"titulo": "vampire", "categoria": "Canción"},
    {"titulo": "Anti-Hero", "categoria": "Canción"},
    {"titulo": "Birds of a Feather", "categoria": "Canción"},
    {"titulo": "Fortnight", "categoria": "Canción"},
    {"titulo": "Midnights", "categoria": "Álbum"},
    {"titulo": "The Tortured Poets Department", "categoria": "Álbum"},
    {"titulo": "Short n' Sweet", "categoria": "Álbum"},
    {"titulo": "SOUR", "categoria": "Álbum"},
    {"titulo": "Taylor Swift", "categoria": "Artista"},
    {"titulo": "Sabrina Carpenter", "categoria": "Artista"},
    {"titulo": "Ariana Grande", "categoria": "Artista"},
    {"titulo": "Milo J", "categoria": "Artista"},
    {"titulo": "Heartstopper: Dos chicos juntos", "categoria": "Libro"},
    {"titulo": "Orgullo y prejuicio", "categoria": "Libro"},
    {"titulo": "Los juegos del hambre", "categoria": "Libro"},
    {"titulo": "Harry Potter y la piedra filosofal", "categoria": "Libro"},
]


CATALOGO_AMPLIADO = [
    # Películas 
    {"titulo": "Nueve reinas", "categoria": "Película"},
    {"titulo": "El secreto de sus ojos", "categoria": "Película"},
    {"titulo": "Relatos salvajes", "categoria": "Película"},
    {"titulo": "Esperando la carroza", "categoria": "Película"},
    {"titulo": "La historia oficial", "categoria": "Película"},
    {"titulo": "Argentina, 1985", "categoria": "Película"},
    {"titulo": "El aura", "categoria": "Película"},
    {"titulo": "Hombre mirando al sudeste", "categoria": "Película"},
    {"titulo": "La ciénaga", "categoria": "Película"},
    {"titulo": "Pizza, birra, faso", "categoria": "Película"},
    {"titulo": "Un cuento chino", "categoria": "Película"},
    {"titulo": "Tiempo de valientes", "categoria": "Película"},
    {"titulo": "El hijo de la novia", "categoria": "Película"},
    {"titulo": "Luna de Avellaneda", "categoria": "Película"},
    {"titulo": "Camila", "categoria": "Película"},
    {"titulo": "La Patagonia rebelde", "categoria": "Película"},
    {"titulo": "El ciudadano ilustre", "categoria": "Película"},
    {"titulo": "Las buenas intenciones", "categoria": "Película"},
    {"titulo": "Cuando acecha la maldad", "categoria": "Película"},
    {"titulo": "Hermanas", "categoria": "Película"},
    {"titulo": "El padrino", "categoria": "Película"},
    {"titulo": "Pulp Fiction", "categoria": "Película"},
    {"titulo": "Interestelar", "categoria": "Película"},
    {"titulo": "Parásitos", "categoria": "Película"},
    {"titulo": "Forrest Gump", "categoria": "Película"},
    {"titulo": "El club de la pelea", "categoria": "Película"},
    {"titulo": "Matrix", "categoria": "Película"},
    {"titulo": "Volver al futuro", "categoria": "Película"},
    {"titulo": "Jurassic Park", "categoria": "Película"},
    {"titulo": "El señor de los anillos: La comunidad del anillo", "categoria": "Película"},
    {"titulo": "Harry Potter y la piedra filosofal", "categoria": "Película"},
    {"titulo": "El diario de una pasión", "categoria": "Película"},
    {"titulo": "El silencio de los inocentes", "categoria": "Película"},
    {"titulo": "Psicosis", "categoria": "Película"},
    {"titulo": "El resplandor", "categoria": "Película"},
    {"titulo": "Coco", "categoria": "Película"},
    {"titulo": "Toy Story", "categoria": "Película"},
    {"titulo": "Whiplash", "categoria": "Película"},
    {"titulo": "El gran hotel Budapest", "categoria": "Película"},
    {"titulo": "Amélie", "categoria": "Película"},
    {"titulo": "Ciudad de Dios", "categoria": "Película"},
    # Series 
    {"titulo": "El encargado", "categoria": "Serie"},
    {"titulo": "Los simuladores", "categoria": "Serie"},
    {"titulo": "Okupas", "categoria": "Serie"},
    {"titulo": "División Palermo", "categoria": "Serie"},
    {"titulo": "Casi feliz", "categoria": "Serie"},
    {"titulo": "Envidiosa", "categoria": "Serie"},
    {"titulo": "Santa Evita", "categoria": "Serie"},
    {"titulo": "Argentina, tierra de amor y venganza", "categoria": "Serie"},
    {"titulo": "The Crown", "categoria": "Serie"},
    {"titulo": "Breaking Bad", "categoria": "Serie"},
    {"titulo": "Better Call Saul", "categoria": "Serie"},
    {"titulo": "Game of Thrones", "categoria": "Serie"},
    {"titulo": "House of the Dragon", "categoria": "Serie"},
    {"titulo": "The Bear", "categoria": "Serie"},
    {"titulo": "Black Mirror", "categoria": "Serie"},
    {"titulo": "Dark", "categoria": "Serie"},
    {"titulo": "The Walking Dead", "categoria": "Serie"},
    {"titulo": "Lost", "categoria": "Serie"},
    {"titulo": "The White Lotus", "categoria": "Serie"},
    {"titulo": "Euphoria", "categoria": "Serie"},
    {"titulo": "The Boys", "categoria": "Serie"},
    {"titulo": "Severance", "categoria": "Serie"},
    {"titulo": "The Queen's Gambit", "categoria": "Serie"},
    {"titulo": "The Good Place", "categoria": "Serie"},
    {"titulo": "Modern Family", "categoria": "Serie"},
    {"titulo": "The Big Bang Theory", "categoria": "Serie"},
    {"titulo": "Anne with an E", "categoria": "Serie"},
    {"titulo": "Bridgerton", "categoria": "Serie"},
    {"titulo": "One Piece", "categoria": "Serie"},
    {"titulo": "El juego del calamar", "categoria": "Serie"},
    # Libros
    {"titulo": "Rayuela", "categoria": "Libro"},
    {"titulo": "Ficciones", "categoria": "Libro"},
    {"titulo": "El Aleph", "categoria": "Libro"},
    {"titulo": "Martín Fierro", "categoria": "Libro"},
    {"titulo": "Sobre héroes y tumbas", "categoria": "Libro"},
    {"titulo": "El túnel", "categoria": "Libro"},
    {"titulo": "Operación Masacre", "categoria": "Libro"},
    {"titulo": "Santa Evita", "categoria": "Libro"},
    {"titulo": "Las cosas que perdimos en el fuego", "categoria": "Libro"},
    {"titulo": "Distancia de rescate", "categoria": "Libro"},
    {"titulo": "Los siete locos", "categoria": "Libro"},
    {"titulo": "La invención de Morel", "categoria": "Libro"},
    {"titulo": "Mafalda", "categoria": "Libro"},
    {"titulo": "El Eternauta", "categoria": "Libro"},
    {"titulo": "Boquitas pintadas", "categoria": "Libro"},
    {"titulo": "1984", "categoria": "Libro"},
    {"titulo": "Un mundo feliz", "categoria": "Libro"},
    {"titulo": "Crimen y castigo", "categoria": "Libro"},
    {"titulo": "Cien años de soledad", "categoria": "Libro"},
    {"titulo": "El amor en los tiempos del cólera", "categoria": "Libro"},
    {"titulo": "Don Quijote de la Mancha", "categoria": "Libro"},
    {"titulo": "Frankenstein", "categoria": "Libro"},
    {"titulo": "Drácula", "categoria": "Libro"},
    {"titulo": "Mujercitas", "categoria": "Libro"},
    {"titulo": "Jane Eyre", "categoria": "Libro"},
    {"titulo": "Cumbres borrascosas", "categoria": "Libro"},
    {"titulo": "El principito", "categoria": "Libro"},
    {"titulo": "Dune", "categoria": "Libro"},
    {"titulo": "Fundación", "categoria": "Libro"},
    {"titulo": "El cuento de la criada", "categoria": "Libro"},
    {"titulo": "It", "categoria": "Libro"},
    {"titulo": "Misery", "categoria": "Libro"},
    {"titulo": "La sombra del viento", "categoria": "Libro"},
    {"titulo": "El nombre de la rosa", "categoria": "Libro"},
    {"titulo": "Persépolis", "categoria": "Libro"},
    {"titulo": "El hobbit", "categoria": "Libro"},
    {"titulo": "Crónicas de Narnia: El león, la bruja y el ropero", "categoria": "Libro"},
    {"titulo": "La naranja mecánica", "categoria": "Libro"},
    {"titulo": "El guardián entre el centeno", "categoria": "Libro"},
    # Directores 
    {"titulo": "Juan José Campanella", "categoria": "Director"},
    {"titulo": "Damián Szifron", "categoria": "Director"},
    {"titulo": "Lucrecia Martel", "categoria": "Director"},
    {"titulo": "Pablo Trapero", "categoria": "Director"},
    {"titulo": "Lisandro Alonso", "categoria": "Director"},
    {"titulo": "María Luisa Bemberg", "categoria": "Director"},
    {"titulo": "Santiago Mitre", "categoria": "Director"},
    {"titulo": "Luis Puenzo", "categoria": "Director"},
    {"titulo": "Martín Rejtman", "categoria": "Director"},
    {"titulo": "Adolfo Aristarain", "categoria": "Director"},
    {"titulo": "Steven Spielberg", "categoria": "Director"},
    {"titulo": "Martin Scorsese", "categoria": "Director"},
    {"titulo": "Christopher Nolan", "categoria": "Director"},
    {"titulo": "Quentin Tarantino", "categoria": "Director"},
    {"titulo": "Greta Gerwig", "categoria": "Director"},
    {"titulo": "Sofia Coppola", "categoria": "Director"},
    {"titulo": "Alfred Hitchcock", "categoria": "Director"},
    {"titulo": "Stanley Kubrick", "categoria": "Director"},
    {"titulo": "Hayao Miyazaki", "categoria": "Director"},
    {"titulo": "Pedro Almodóvar", "categoria": "Director"},
    {"titulo": "Bong Joon-ho", "categoria": "Director"},
    {"titulo": "Wes Anderson", "categoria": "Director"},
    {"titulo": "Denis Villeneuve", "categoria": "Director"},
    {"titulo": "Agnès Varda", "categoria": "Director"},
    {"titulo": "Guillermo del Toro", "categoria": "Director"},
    # Escritores argentinos e internacionales
    {"titulo": "Jorge Luis Borges", "categoria": "Escritor"},
    {"titulo": "Julio Cortázar", "categoria": "Escritor"},
    {"titulo": "María Elena Walsh", "categoria": "Escritor"},
    {"titulo": "Ernesto Sabato", "categoria": "Escritor"},
    {"titulo": "Adolfo Bioy Casares", "categoria": "Escritor"},
    {"titulo": "Silvina Ocampo", "categoria": "Escritor"},
    {"titulo": "Manuel Puig", "categoria": "Escritor"},
    {"titulo": "Roberto Arlt", "categoria": "Escritor"},
    {"titulo": "Selva Almada", "categoria": "Escritor"},
    {"titulo": "Samanta Schweblin", "categoria": "Escritor"},
    {"titulo": "Mariana Enríquez", "categoria": "Escritor"},
    {"titulo": "Claudia Piñeiro", "categoria": "Escritor"},
    {"titulo": "Eduardo Sacheri", "categoria": "Escritor"},
    {"titulo": "José Hernández", "categoria": "Escritor"},
    {"titulo": "Liliana Bodoc", "categoria": "Escritor"},
    {"titulo": "William Shakespeare", "categoria": "Escritor"},
    {"titulo": "Jane Austen", "categoria": "Escritor"},
    {"titulo": "Mary Shelley", "categoria": "Escritor"},
    {"titulo": "George Orwell", "categoria": "Escritor"},
    {"titulo": "J. R. R. Tolkien", "categoria": "Escritor"},
    {"titulo": "J. K. Rowling", "categoria": "Escritor"},
    {"titulo": "Stephen King", "categoria": "Escritor"},
    {"titulo": "Agatha Christie", "categoria": "Escritor"},
    {"titulo": "Gabriel García Márquez", "categoria": "Escritor"},
    {"titulo": "Isabel Allende", "categoria": "Escritor"},
    {"titulo": "Haruki Murakami", "categoria": "Escritor"},
    {"titulo": "Virginia Woolf", "categoria": "Escritor"},
    {"titulo": "Franz Kafka", "categoria": "Escritor"},
    {"titulo": "Fyodor Dostoevsky", "categoria": "Escritor"},
    {"titulo": "Octavia E. Butler", "categoria": "Escritor"},
]

# Mantiene el catálogo original y agrega los nuevos elementos una sola vez.
_titulos_existentes = {(x["titulo"].casefold(), x["categoria"]) for x in CATALOGO}

for _item in CATALOGO_AMPLIADO:
    _clave = (_item["titulo"].casefold(), _item["categoria"])
    if _clave not in _titulos_existentes:
        CATALOGO.append(_item)
        _titulos_existentes.add(_clave)
        
# Descripciones breves del catálogo.
DESCRIPCIONES = {
    "Barbie": "Comedia fantástica en la que Barbie deja Barbielandia y se enfrenta a preguntas sobre identidad, expectativas y el mundo real.",
"Intensamente 2": "Riley atraviesa la adolescencia y descubre nuevas emociones que complican el equilibrio de su mundo interior.",
"Spider-Man: No Way Home": "Peter Parker busca revertir las consecuencias de que el mundo conozca su identidad y se enfrenta a visitantes de otros universos.",
"Orgullo y prejuicio": "La novela de Jane Austen retrata a Elizabeth Bennet y Darcy, explorando el amor, los prejuicios y las diferencias sociales.",
"10 cosas que odio de ti": "Comedia romántica adolescente inspirada libremente en Shakespeare, sobre dos hermanas, reglas familiares y un romance inesperado.",
"La La Land": "Musical romántico sobre una aspirante a actriz y un músico de jazz que persiguen sus sueños en Los Ángeles.",
"El viaje de Chihiro": "Una niña entra en un mundo mágico habitado por espíritus y debe encontrar el valor para salvar a sus padres y volver a casa.",
"Titanic": "Drama romántico ambientado en el viaje del transatlántico Titanic, que combina una historia de amor con una tragedia histórica.",
"Stranger Things": "Un grupo de chicos de un pueblo de Indiana descubre experimentos secretos y una dimensión aterradora tras la desaparición de un amigo.",
"Merlina": "Merlina Addams investiga misterios y crímenes mientras estudia en la Academia Nunca Más y descubre secretos de su familia.",
"El verano en que me enamoré": "Drama juvenil sobre Belly, sus vínculos afectivos y los cambios que vive durante los veranos junto a una familia cercana.",
"Heartstopper": "Historia de crecimiento y romance sobre Charlie y Nick, que explora la amistad, la identidad y el primer amor.",
"The Office": "Comedia en formato de falso documental que sigue las situaciones absurdas y las relaciones entre compañeros de una oficina.",
"The Last of Us": "Tras una pandemia que transforma el mundo, Joel acompaña a Ellie en un peligroso viaje donde surgen vínculos y dilemas morales.",
"Gilmore Girls": "Comedia dramática sobre Lorelai y Rory Gilmore, madre e hija unidas por conversaciones rápidas, sueños y la vida de un pequeño pueblo.",
"Friends": "Comedia sobre seis amigos de Nueva York que atraviesan relaciones, trabajo y cambios personales mientras se acompañan.",
"Cruel Summer": "Canción de Taylor Swift que combina una producción pop intensa con la emoción de un romance apasionado y complicado.",
"Espresso": "Tema pop de Sabrina Carpenter, de ritmo ligero y actitud juguetona, sobre sentirse irresistible y permanecer en la mente de alguien.",
"vampire": "Balada pop-rock de Olivia Rodrigo sobre la decepción, la manipulación y el enojo tras una relación desigual.",
"Anti-Hero": "Canción introspectiva de Taylor Swift que aborda inseguridades, contradicciones personales y la autocrítica.",
"Birds of a Feather": "Canción de Billie Eilish sobre un amor profundo y el deseo de permanecer junto a otra persona.",
"Fortnight": "Tema de Taylor Swift con Post Malone que evoca una relación breve, la nostalgia y los sentimientos que persisten.",
"Midnights": "Álbum de Taylor Swift inspirado en pensamientos nocturnos, recuerdos, inseguridades y distintas etapas de la vida.",
"The Tortured Poets Department": "Álbum de Taylor Swift centrado en rupturas, contradicciones emocionales y el uso de la escritura para procesar experiencias.",
"Short n' Sweet": "Álbum de Sabrina Carpenter con pop melódico, humor y canciones sobre romances, deseo y desilusiones.",
"SOUR": "Álbum debut de Olivia Rodrigo que mezcla pop y pop-rock para expresar desamor, frustración y emociones adolescentes.",
"Taylor Swift": "Cantautora estadounidense que combina pop, country y folk, reconocida por sus letras narrativas y álbumes conceptuales.",
"Sabrina Carpenter": "Cantante y actriz estadounidense de pop, conocida por su voz, sus letras ingeniosas y sus estribillos pegadizos.",
"Ariana Grande": "Cantante y actriz estadounidense reconocida por su amplio registro vocal y su combinación de pop y R&B.",
"Milo J": "Cantante y compositor argentino que mezcla rap, música urbana y sonidos melódicos con letras personales.",
"Heartstopper: Dos chicos juntos": "Novela gráfica de Alice Oseman sobre Charlie y Nick, dos estudiantes que construyen una amistad que se transforma en amor.",
"Los juegos del hambre": "En una sociedad autoritaria, Katniss Everdeen debe sobrevivir a un espectáculo mortal que también despierta una rebelión.",
"Harry Potter y la piedra filosofal": "Primer libro de la saga: Harry descubre que es mago y comienza sus estudios en Hogwarts, donde encuentra amistad y misterio.",
"Nueve reinas": "Dos estafadores porteños se asocian para vender una supuesta colección de estampillas raras en una trama de engaños y giros.",
"El secreto de sus ojos": "Un empleado judicial jubilado escribe sobre un caso de asesinato que marcó su vida y un amor que quedó pendiente.",
"Relatos salvajes": "Película antológica de humor negro en la que personas comunes llegan al límite ante situaciones injustas o absurdas.",
"Esperando la carroza": "Comedia argentina de enredos familiares que satiriza la hipocresía y las tensiones de una familia reunida.",
"La historia oficial": "Una profesora empieza a cuestionar el origen de su hija adoptiva durante los últimos años de la dictadura argentina.",
"Argentina, 1985": "Drama histórico inspirado en el juicio a las juntas militares responsables de crímenes durante la última dictadura.",
"El aura": "Un taxidermista reservado, con una memoria extraordinaria, se ve involucrado en un plan criminal que se descontrola.",
"Hombre mirando al sudeste": "Un médico psiquiatra conoce a un paciente que afirma venir de otro planeta y cuestiona la lógica de la institución.",
"La ciénaga": "Drama de Lucrecia Martel sobre dos familias del noroeste argentino, sus tensiones, decadencia y silencios cotidianos.",
"Pizza, birra, faso": "Retrato urbano de jóvenes en Buenos Aires que sobreviven mediante pequeños delitos y sueñan con escapar de su realidad.",
"Un cuento chino": "Un ferretero solitario ve alterada su rutina cuando un joven chino aparece inesperadamente en su vida.",
"Tiempo de valientes": "Comedia policial sobre un psicólogo obligado a acompañar a un policía en una investigación llena de situaciones disparatadas.",
"El hijo de la novia": "Un dueño de restaurante en crisis reconsidera sus prioridades familiares cuando su padre quiere cumplir un viejo sueño.",
"Luna de Avellaneda": "Un club de barrio lucha por sobrevivir y sus socios deben decidir entre conservar su identidad o aceptar una salida económica.",
"Camila": "Drama histórico basado en el romance prohibido entre Camila O’Gorman y el sacerdote Ladislao Gutiérrez en el siglo XIX.",
"La Patagonia rebelde": "Película histórica sobre las huelgas de trabajadores rurales patagónicos y la represión de comienzos de la década de 1920.",
"El ciudadano ilustre": "Un escritor argentino premiado internacionalmente vuelve a su pueblo natal y se enfrenta a viejos conflictos y resentimientos.",
"Las buenas intenciones": "Drama familiar sobre una niña que observa las dificultades de sus padres y trata de encontrar su lugar entre ellos.",
"Cuando acecha la maldad": "Película de terror rural en la que dos hermanos se enfrentan a una presencia demoníaca que amenaza a su comunidad.",
"Hermanas": "Drama sobre dos hermanas argentinas que se reencuentran en el exilio y deben enfrentar recuerdos familiares y políticos.",
"El padrino": "Crónica de la familia Corleone y de la sucesión dentro de una organización mafiosa, centrada en poder, lealtad y violencia.",
"Pulp Fiction": "Película de historias entrelazadas sobre criminales y personajes de Los Ángeles, narrada con humor negro y estructura no lineal.",
"Interestelar": "Un grupo de astronautas viaja más allá de la Tierra para buscar un futuro para la humanidad mientras el tiempo adquiere un papel crucial.",
"Parásitos": "Thriller satírico sobre una familia con pocos recursos que se introduce gradualmente en la vida de una familia adinerada.",
"Forrest Gump": "Un hombre de mirada sencilla atraviesa acontecimientos importantes de la historia estadounidense mientras busca el amor y la pertenencia.",
"El club de la pelea": "Un hombre insatisfecho crea junto a un misterioso conocido un club clandestino que termina convirtiéndose en algo peligroso.",
"Matrix": "Un programador descubre que la realidad cotidiana es una simulación y se une a una lucha contra quienes la controlan.",
"Volver al futuro": "Un adolescente viaja accidentalmente al pasado en un automóvil convertido en máquina del tiempo y debe proteger su propia existencia.",
"Jurassic Park": "Un parque temático con dinosaurios clonados pierde el control de sus sistemas y convierte la visita en una lucha por sobrevivir.",
"El señor de los anillos: La comunidad del anillo": "Frodo emprende una misión para destruir un anillo de poder acompañado por un grupo de aliados de distintas razas.",
"El diario de una pasión": "Dos jóvenes de orígenes distintos viven un romance marcado por las diferencias sociales, el paso del tiempo y la memoria.",
"El silencio de los inocentes": "Una joven agente del FBI busca la ayuda de un brillante asesino encarcelado para atrapar a otro criminal.",
"Psicosis": "Un thriller de Alfred Hitchcock sobre una mujer que llega a un motel aislado y descubre un misterio inquietante.",
"El resplandor": "Un escritor acepta cuidar un hotel aislado durante el invierno y su familia comienza a sufrir sucesos perturbadores.",
"Coco": "Un niño mexicano apasionado por la música llega al mundo de los muertos y descubre secretos de su historia familiar.",
"Toy Story": "Los juguetes de un niño cobran vida cuando nadie los ve y deben adaptarse a la llegada de un nuevo favorito.",
"Whiplash": "Un joven baterista busca la excelencia bajo la exigencia extrema de un profesor de música.",
"El gran hotel Budapest": "Un conserje y su joven ayudante se ven envueltos en un robo, una herencia y aventuras en una Europa ficticia.",
"Amélie": "Una joven parisina decide mejorar discretamente la vida de quienes la rodean mientras aprende a afrontar sus propios deseos.",
"Ciudad de Dios": "Drama brasileño que sigue a jóvenes de una favela de Río de Janeiro y el crecimiento de la violencia y el crimen organizado.",
"El encargado": "Comedia negra argentina sobre un encargado de edificio que manipula a los residentes para conservar el control.",
"Los simuladores": "Cuatro especialistas resuelven problemas ajenos mediante operativos elaborados, disfraces y engaños cuidadosamente planeados.",
"Okupas": "Serie argentina que sigue a un joven que ocupa una casa y se acerca a un grupo de amigos en los márgenes de Buenos Aires.",
"División Palermo": "Comedia policial sobre una guardia urbana inclusiva que se enfrenta a situaciones absurdas y a un delito más complejo de lo esperado.",
"Casi feliz": "Comedia dramática sobre un conductor de radio que intenta reconstruir su vida sentimental y familiar tras una separación.",
"Envidiosa": "Comedia dramática argentina sobre una mujer que revisa sus expectativas de pareja, éxito y vida al compararse con los demás.",
"Santa Evita": "Drama histórico que explora el destino del cuerpo embalsamado de Eva Perón y el impacto político de su figura.",
"Argentina, tierra de amor y venganza": "Telenovela histórica ambientada entre inmigrantes en la Argentina de los años treinta, con romances, secretos y conflictos.",
"The Crown": "Drama histórico sobre el reinado de Isabel II y las tensiones entre la familia real británica, la política y la vida privada.",
"Breaking Bad": "Un profesor de química diagnosticado con cáncer comienza a fabricar metanfetamina y se transforma progresivamente en criminal.",
"Better Call Saul": "Precuela de Breaking Bad que sigue la transformación del abogado Jimmy McGill en el astuto Saul Goodman.",
"Game of Thrones": "Familias nobles compiten por el poder en Westeros mientras amenazas sobrenaturales crecen más allá de sus fronteras.",
"House of the Dragon": "Drama fantástico sobre la familia Targaryen y la disputa sucesoria que conduce a una guerra civil.",
"The Bear": "Un joven chef vuelve a Chicago para hacerse cargo del restaurante familiar y enfrenta duelo, presión laboral y vínculos difíciles.",
"Black Mirror": "Antología de historias independientes que examinan los efectos inquietantes de la tecnología y la sociedad contemporánea.",
"Dark": "La desaparición de un niño en un pueblo alemán revela secretos familiares y una compleja trama de viajes en el tiempo.",
"The Walking Dead": "Un grupo de sobrevivientes intenta reconstruir una vida en un mundo devastado por los muertos vivientes.",
"Lost": "Los sobrevivientes de un accidente aéreo quedan varados en una isla llena de misterios y secretos.",
"The White Lotus": "Sátira dramática sobre huéspedes y empleados de resorts de lujo, donde privilegio y tensiones personales desembocan en conflictos.",
"Euphoria": "Drama juvenil que retrata relaciones, adicciones, identidad y salud emocional a través de un grupo de estudiantes.",
"The Boys": "En un mundo donde los superhéroes son celebridades corruptibles, un grupo busca exponer sus abusos de poder.",
"Severance": "Empleados se someten a un procedimiento que separa sus recuerdos laborales de los personales, con consecuencias inquietantes.",
"The Queen's Gambit": "Una joven prodigio del ajedrez asciende en un mundo competitivo mientras lucha con sus propias dependencias y soledad.",
"The Good Place": "Una mujer llega por error a una aparente utopía después de morir y trata de aprender qué significa ser buena persona.",
"Modern Family": "Comedia coral sobre tres ramas de una familia que atraviesan situaciones cotidianas con estilos y generaciones diferentes.",
"The Big Bang Theory": "Comedia sobre un grupo de científicos y sus amistades, romances y dificultades para interpretar las convenciones sociales.",
"Anne with an E": "Una niña imaginativa y huérfana encuentra un hogar en un pueblo rural y transforma la vida de quienes la rodean.",
"Bridgerton": "Romance de época sobre familias de la alta sociedad londinense, sus temporadas sociales, secretos y relaciones amorosas.",
"One Piece": "Un joven pirata y su tripulación recorren los mares en busca de un tesoro legendario y aventuras.",
"El juego del calamar": "Personas endeudadas participan en juegos infantiles mortales por un premio, exponiendo desigualdades y desesperación.",
"Rayuela": "Novela experimental de Julio Cortázar que invita a leer sus capítulos en distintos órdenes y explora el amor, el azar y la búsqueda existencial.",
"Ficciones": "Colección de relatos de Jorge Luis Borges sobre laberintos, bibliotecas, espejos, identidades y paradojas filosóficas.",
"El Aleph": "Libro de cuentos de Borges que combina lo fantástico y lo filosófico; el relato titular presenta un punto que contiene todo el universo.",
"Martín Fierro": "Poema narrativo de José Hernández sobre un gaucho perseguido por la autoridad y la vida en la frontera argentina.",
"Sobre héroes y tumbas": "Novela de Ernesto Sabato que entrelaza una historia amorosa con reflexiones sobre la sociedad y la condición humana.",
"El túnel": "Novela psicológica narrada por un pintor que intenta explicar el crimen que cometió y su obsesión amorosa.",
"Operación Masacre": "Investigación narrativa de Rodolfo Walsh sobre fusilamientos clandestinos ocurridos en 1956 en Argentina.",
"Santa Evita": "Novela de Tomás Eloy Martínez que mezcla historia y ficción alrededor del cuerpo de Eva Perón y su mito político.",
"Las cosas que perdimos en el fuego": "Cuentos de Mariana Enríquez que combinan terror con violencia social, desigualdad y miedos contemporáneos.",
"Distancia de rescate": "Novela breve de Samanta Schweblin que construye una atmósfera inquietante alrededor de la maternidad y el peligro ambiental.",
"Los siete locos": "Novela de Roberto Arlt sobre un hombre desesperado que se involucra con personajes que imaginan proyectos extremos para cambiar la sociedad.",
"La invención de Morel": "Un fugitivo llega a una isla donde los habitantes parecen repetir una rutina inexplicable, en una novela fantástica de Bioy Casares.",
"Mafalda": "Historieta de Quino protagonizada por una niña curiosa que cuestiona la política, la sociedad y el mundo adulto con humor.",
"El Eternauta": "Historieta argentina de ciencia ficción en la que una nevada mortal anuncia una invasión extraterrestre en Buenos Aires.",
"Boquitas pintadas": "Novela de Manuel Puig construida con cartas, voces y documentos que revelan amores, apariencias y secretos de un pueblo.",
"1984": "Distopía de George Orwell sobre un régimen totalitario que vigila a la población y controla el lenguaje y la memoria.",
"Un mundo feliz": "Distopía de Aldous Huxley sobre una sociedad organizada mediante condicionamiento, consumo y una felicidad controlada.",
"Crimen y castigo": "Novela de Dostoievski sobre un estudiante que comete un asesinato y queda atrapado en la culpa y el conflicto moral.",
"Cien años de soledad": "Saga de la familia Buendía en Macondo, donde historia, memoria y hechos fantásticos se entrelazan durante generaciones.",
"El amor en los tiempos del cólera": "Historia de un amor persistente que atraviesa décadas, cambios sociales y distintas formas de esperar.",
"Don Quijote de la Mancha": "Clásico de Cervantes sobre un hidalgo que, inspirado por libros de caballería, sale a recorrer el mundo como caballero andante.",
"Frankenstein": "Novela de Mary Shelley sobre un científico que crea vida y debe afrontar las consecuencias de abandonar a su criatura.",
"Drácula": "Novela epistolar de Bram Stoker sobre la amenaza de un vampiro y los esfuerzos de un grupo por detenerlo.",
"Mujercitas": "Historia de las hermanas March, que crecen, trabajan y buscan sus propios caminos durante la Guerra Civil estadounidense.",
"Jane Eyre": "Novela de Charlotte Brontë sobre una joven huérfana que busca independencia, amor y dignidad.",
"Cumbres borrascosas": "Novela de Emily Brontë sobre una pasión intensa y destructiva que afecta a dos familias a lo largo de generaciones.",
"El principito": "Relato poético de Antoine de Saint-Exupéry sobre un niño viajero que reflexiona sobre el afecto, la amistad y lo esencial.",
"Dune": "Ciencia ficción de Frank Herbert sobre poder, ecología y religión en el planeta desértico Arrakis, fuente de una sustancia valiosa.",
"Fundación": "Saga de Isaac Asimov sobre un plan científico para preservar el conocimiento y acortar una futura era de caos galáctico.",
"El cuento de la criada": "Distopía de Margaret Atwood sobre una sociedad autoritaria que controla los cuerpos y la reproducción de las mujeres.",
"It": "Novela de Stephen King en la que un grupo de amigos se enfrenta a una entidad aterradora que acecha en su pueblo.",
"Misery": "Un escritor herido queda bajo el cuidado de una admiradora obsesiva que lo obliga a escribir según sus deseos.",
"La sombra del viento": "Un joven descubre un libro olvidado en Barcelona y comienza a investigar el misterio de su autor.",
"El nombre de la rosa": "Un fraile franciscano investiga muertes misteriosas en una abadía medieval, entre disputas religiosas y secretos bibliográficos.",
"Persépolis": "Novela gráfica autobiográfica de Marjane Satrapi sobre crecer en Irán durante la revolución y vivir entre culturas.",
"El hobbit": "Bilbo Bolsón se une a un grupo de enanos en una aventura para recuperar su reino y su tesoro de un dragón.",
"Crónicas de Narnia: El león, la bruja y el ropero": "Cuatro hermanos descubren un mundo mágico dominado por una bruja y ayudan a restaurar su libertad.",
"La naranja mecánica": "Novela de Anthony Burgess sobre violencia juvenil, libre albedrío y los límites éticos del control estatal.",
"El guardián entre el centeno": "Novela de J. D. Salinger narrada por un adolescente que expresa alienación, duelo y rechazo a la hipocresía adulta.",
"Juan José Campanella": "Director y guionista argentino conocido por combinar emoción, humor y temas sociales; dirigió El secreto de sus ojos y El hijo de la novia.",
"Damián Szifron": "Director y guionista argentino reconocido por Relatos salvajes y por crear la serie Los simuladores.",
"Lucrecia Martel": "Directora argentina de cine de autor, destacada por su trabajo sobre la familia, la clase social y los sonidos cotidianos.",
"Pablo Trapero": "Director argentino asociado al Nuevo Cine Argentino, con películas como Mundo grúa, El bonaerense y El clan.",
"Lisandro Alonso": "Cineasta argentino conocido por películas contemplativas que exploran el territorio, el tiempo y la experiencia humana.",
"María Luisa Bemberg": "Directora y guionista argentina que abordó la autonomía de las mujeres y las restricciones sociales en filmes como Camila.",
"Santiago Mitre": "Director y guionista argentino de películas como El estudiante, La cordillera y Argentina, 1985.",
"Luis Puenzo": "Director argentino de La historia oficial, película que aborda la apropiación de niños durante la dictadura.",
"Martín Rejtman": "Director y escritor argentino de estilo minimalista, conocido por observar con humor seco la vida urbana cotidiana.",
"Adolfo Aristarain": "Director y guionista argentino de películas como Un lugar en el mundo y Martín (Hache), centradas en vínculos y dilemas éticos.",
"Steven Spielberg": "Director estadounidense detrás de clásicos de aventura, ciencia ficción y drama como Jurassic Park, E.T. y La lista de Schindler.",
"Martin Scorsese": "Director estadounidense conocido por dramas sobre crimen, ambición y culpa, como Taxi Driver, Buenos muchachos y Los infiltrados.",
"Christopher Nolan": "Director y guionista británico-estadounidense reconocido por narrativas complejas y películas como Interestelar, Origen y Oppenheimer.",
"Quentin Tarantino": "Director y guionista estadounidense de diálogos distintivos, violencia estilizada y relatos no lineales, como Pulp Fiction.",
"Greta Gerwig": "Directora, guionista y actriz estadounidense que explora identidad y crecimiento en Lady Bird, Mujercitas y Barbie.",
"Sofia Coppola": "Directora y guionista estadounidense conocida por retratos íntimos de personajes aislados y películas como Lost in Translation.",
"Alfred Hitchcock": "Director británico-estadounidense, figura clave del suspenso, conocido por Psicosis, Vértigo y La ventana indiscreta.",
"Stanley Kubrick": "Director estadounidense reconocido por su precisión visual y películas como 2001: Odisea del espacio, El resplandor y La naranja mecánica.",
"Hayao Miyazaki": "Director y animador japonés, cofundador de Studio Ghibli, creador de mundos imaginativos como los de El viaje de Chihiro.",
"Pedro Almodóvar": "Director y guionista español cuyas películas exploran deseo, familia, identidad y melodrama con colores y personajes expresivos.",
"Bong Joon-ho": "Director surcoreano que combina géneros y crítica social en películas como Parásitos, Memories of Murder y The Host.",
"Wes Anderson": "Director estadounidense conocido por composiciones simétricas, paletas distintivas y humor excéntrico en películas como El gran hotel Budapest.",
"Denis Villeneuve": "Director canadiense de cine visualmente ambicioso, responsable de Arrival, Blade Runner 2049 y Dune.",
"Agnès Varda": "Directora francesa pionera de la Nouvelle Vague, reconocida por su mirada humanista y su mezcla de documental y ficción.",
"Guillermo del Toro": "Director mexicano que combina fantasía, monstruos y sensibilidad humana en obras como El laberinto del fauno y La forma del agua.",
"Jorge Luis Borges": "Escritor argentino fundamental del siglo XX, famoso por cuentos que exploran laberintos, bibliotecas, tiempo e infinitos.",
"Julio Cortázar": "Escritor argentino de cuentos y novelas experimentales, autor de Rayuela y de relatos fantásticos como Casa tomada.",
"María Elena Walsh": "Escritora, poeta y compositora argentina, creadora de canciones y libros infantiles que marcaron generaciones.",
"Ernesto Sabato": "Escritor argentino autor de El túnel y Sobre héroes y tumbas, con una obra centrada en la angustia y los dilemas humanos.",
"Adolfo Bioy Casares": "Escritor argentino asociado a la literatura fantástica y la ciencia ficción; escribió La invención de Morel.",
"Silvina Ocampo": "Escritora argentina de cuentos y poesía, reconocida por su imaginación inquietante y sus perspectivas poco convencionales.",
"Manuel Puig": "Novelista argentino que incorporó diálogos, cartas y cultura popular en obras como Boquitas pintadas y El beso de la mujer araña.",
"Roberto Arlt": "Novelista y dramaturgo argentino que retrató la ciudad, la marginalidad y personajes inconformes en Los siete locos.",
"Selva Almada": "Escritora argentina contemporánea que aborda la vida rural, la violencia y los vínculos familiares con prosa precisa.",
"Samanta Schweblin": "Escritora argentina de cuentos y novelas inquietantes, autora de Distancia de rescate y Pájaros en la boca.",
"Mariana Enríquez": "Escritora argentina que combina terror y realismo social para explorar violencia, desigualdad y memoria.",
"Claudia Piñeiro": "Escritora y dramaturga argentina, autora de novelas policiales y sociales como Las viudas de los jueves y Elena sabe.",
"Eduardo Sacheri": "Escritor argentino conocido por relatos sobre fútbol, memoria y relaciones humanas; su obra inspiró El secreto de sus ojos.",
"José Hernández": "Poeta y periodista argentino, autor de Martín Fierro, obra central de la literatura gauchesca.",
"Liliana Bodoc": "Escritora argentina de literatura fantástica, reconocida por La saga de los confines y sus mundos inspirados en culturas originarias.",
"William Shakespeare": "Dramaturgo y poeta inglés cuyas tragedias y comedias, como Hamlet y Romeo y Julieta, siguen influyendo en la cultura.",
"Jane Austen": "Novelista inglesa que observó con ironía las relaciones, el matrimonio y las clases sociales; escribió Orgullo y prejuicio.",
"Mary Shelley": "Escritora inglesa autora de Frankenstein, novela fundacional de la ciencia ficción que plantea preguntas sobre creación y responsabilidad.",
"George Orwell": "Escritor y periodista británico, autor de las distopías 1984 y Rebelión en la granja sobre poder y autoritarismo.",
"J. R. R. Tolkien": "Escritor británico creador de la Tierra Media y autor de El hobbit y El señor de los anillos.",
"J. K. Rowling": "Escritora británica creadora de la saga Harry Potter, centrada en magia, amistad, crecimiento y lucha contra el autoritarismo.",
"Stephen King": "Escritor estadounidense de terror y suspenso, autor de It, Misery y numerosas historias sobre miedos cotidianos.",
"Agatha Christie": "Autora británica célebre por sus novelas policiales, con detectives como Hércules Poirot y Miss Marple.",
"Gabriel García Márquez": "Escritor colombiano y figura del realismo mágico, autor de Cien años de soledad y El amor en los tiempos del cólera.",
"Isabel Allende": "Escritora chilena conocida por novelas que combinan memoria, historia familiar y elementos mágicos, como La casa de los espíritus.",
"Haruki Murakami": "Escritor japonés cuyas novelas mezclan vida cotidiana, soledad, música y elementos surrealistas.",
"Virginia Woolf": "Escritora modernista británica, reconocida por su exploración de la conciencia y obras como La señora Dalloway.",
"Franz Kafka": "Escritor de lengua alemana nacido en Praga, conocido por relatos sobre burocracia, alienación y situaciones absurdas.",
"Fyodor Dostoevsky": "Novelista ruso que exploró la culpa, la fe y los conflictos morales en obras como Crimen y castigo.",
"Octavia E. Butler": "Escritora estadounidense pionera de la ciencia ficción, cuyas obras examinan poder, raza, género y supervivencia.",

}

DESCRIPCION_POR_CATEGORIA = {
    "Película": "Obra cinematográfica titulada {titulo}. Podés explorar su historia, personajes, dirección, temas y el efecto que te produjo.",
    "Serie": "Producción episódica titulada {titulo}. Podés comentar la evolución de sus personajes, el ritmo, los temas y las temporadas.",
    "Canción": "Tema musical titulado {titulo}. Podés analizar su letra, sonido, interpretación y las emociones que transmite.",
    "Álbum": "Lanzamiento musical titulado {titulo}. Podés explorar su estilo, sus canciones, la producción y la coherencia del conjunto.",
    "Artista": "Artista musical {titulo}. Podés conocer su trayectoria, estilo, influencias y principales trabajos.",
    "Libro": "Obra literaria titulada {titulo}. Podés explorar su argumento, personajes, estilo narrativo y temas principales.",
    "Director": "Director/a {titulo}. Podés descubrir su trayectoria, estilo visual, temas recurrentes y obras destacadas.",
    "Escritor": "Escritor/a {titulo}. Podés conocer su trayectoria, estilo, temas recurrentes y obras más reconocidas.",
}

for _item in CATALOGO:
    _item["descripcion"] = DESCRIPCIONES.get(
        _item["titulo"],
        DESCRIPCION_POR_CATEGORIA.get(_item["categoria"], "Elemento cultural {titulo}. Podés explorar sus características y compartir tu opinión.").format(titulo=_item["titulo"])
    )
RECOMENDACIONES = [
    ("Harry Potter y el cáliz de fuego", "Película", "Analizá desde la construcción de la trama hasta las escenas más memorables."),
    ("The Office", "Serie", "Una buena opción para reseñar el humor y los personajes."),
    ("El viaje de Chihiro", "Película", "Explora el crecimiento personal, la identidad, la creatividad y la valentía."),
    ("Los juegos del hambre (2008)", "Libro", " Una crítica social sobre la desigualdad, el poder y la supervivencia."),
    ("Canción para mi muerte", "Canción", "Reseñá la letra y qué sensación te transmite."),
    ("10 cosas que odio de ti", "Película", "Podés reseñar sus personajes y su historia."),
    ("La vida era más corta", "Álbum", "Comentá acerca de las letras y el significado que le das."),
    ("Pretty Little Liars", "Serie", "Opiná el misterio, la música y la evolución de la historia."),
    ("Orgullo y prejuicio", "Libro", "Una opción para opinar sobre los personajes y la profunda narración."),
    ("YHLQMDLG (2020)", "Álbum", "Canciones que van desde la fiesta hasta experiencias personales, como el desamor."),
    ("Stranger Things", "Serie", "Comentá el misterio, la música y la evolución de la historia."),
    ("Los del Fuego", "Artista", "Opiná sobre sus interpretaciones y su importancia dentro de la cultura popular argentina."),
]

CATEGORIAS = ["Película", "Serie", "Director", "Canción", "Álbum", "Artista", "Libro", "Escritor"]

# Estado de la sesión actual. Los datos se guardan en SQLite.

usuario_actual = ""

modo_actual = "Espectador"

vista_previa_espectador = False

def conectar():
    con = sqlite3.connect(DB_ARCHIVO)
    con.execute("PRAGMA foreign_keys = ON")
    return con
def columnas_tabla(con, tabla):
    return {fila[1] for fila in con.execute(f"PRAGMA table_info({tabla})").fetchall()}
def inicializar_bd():
    """Crea las tablas y adapta una base de datos anterior sin borrar sus datos."""
    try:
        with conectar() as con:
            con.execute("""
                CREATE TABLE IF NOT EXISTS resenas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    puntuacion INTEGER NOT NULL,
                    comentario TEXT,
                    favorito INTEGER NOT NULL DEFAULT 0,
                    fecha TEXT NOT NULL
                )
            """)
            cols = columnas_tabla(con, "resenas")
            if "autor" not in cols:
                con.execute("ALTER TABLE resenas ADD COLUMN autor TEXT NOT NULL DEFAULT 'Usuario anterior'")
            if "publica" not in cols:
                con.execute("ALTER TABLE resenas ADD COLUMN publica INTEGER NOT NULL DEFAULT 1")
            con.execute("""
                CREATE TABLE IF NOT EXISTS listas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    autor TEXT NOT NULL DEFAULT 'Usuario'
                )
            """)
            if "autor" not in columnas_tabla(con, "listas"):
                con.execute("ALTER TABLE listas ADD COLUMN autor TEXT NOT NULL DEFAULT 'Usuario'")
            con.execute("""
                CREATE TABLE IF NOT EXISTS elementos_lista (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lista_id INTEGER,
                    titulo_elemento TEXT NOT NULL,
                    FOREIGN KEY (lista_id) REFERENCES listas(id) ON DELETE CASCADE
                )
            """)
            con.execute("""
                CREATE TABLE IF NOT EXISTS comentarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    resena_id INTEGER NOT NULL,
                    autor TEXT NOT NULL,
                    texto TEXT NOT NULL,
                    fecha TEXT NOT NULL,
                    respuesta_a INTEGER,
                    FOREIGN KEY (resena_id) REFERENCES resenas(id) ON DELETE CASCADE,
                    FOREIGN KEY (respuesta_a) REFERENCES comentarios(id) ON DELETE CASCADE
                )
            """)
            con.execute("""
                CREATE TABLE IF NOT EXISTS reacciones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    resena_id INTEGER NOT NULL,
                    autor TEXT NOT NULL,
                    tipo TEXT NOT NULL DEFAULT '❤️',
                    UNIQUE(resena_id, autor),
                    FOREIGN KEY (resena_id) REFERENCES resenas(id) ON DELETE CASCADE
                )
            """)
            con.execute("""
                CREATE TABLE IF NOT EXISTS busquedas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    consulta TEXT NOT NULL,
                    autor TEXT NOT NULL,
                    fecha TEXT NOT NULL
                )
            """)
            con.execute("""
                CREATE TABLE IF NOT EXISTS catalogo_aprobado (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    UNIQUE(titulo, categoria)
                )
            """)
            con.execute("""
                CREATE TABLE IF NOT EXISTS propuestas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    autor TEXT NOT NULL,
                    fecha TEXT NOT NULL,
                    estado TEXT NOT NULL DEFAULT 'Pendiente'
                )
            """)
            con.execute("""
                CREATE TABLE IF NOT EXISTS ajustes (
                    clave TEXT PRIMARY KEY,
                    valor TEXT NOT NULL
                )
            """)
    except sqlite3.Error as e:
        messagebox.showerror("Error de base de datos", f"No se pudo inicializar la base de datos:\n{e}")
def obtener_resenas(autor=None, solo_favoritos=False, publicas=False):
    sql = """SELECT id, titulo, categoria, puntuacion, comentario, favorito, fecha,
                    COALESCE(autor, 'Usuario anterior'), COALESCE(publica, 1)
             FROM resenas WHERE 1=1"""
    params = []
    if autor is not None:
        sql += " AND autor = ?"
        params.append(autor)
    if solo_favoritos:
        sql += " AND favorito = 1 AND autor = ?"
        params.append(usuario_actual)
    if publicas:
        sql += " AND publica = 1"
    sql += " ORDER BY id DESC"
    with conectar() as con:
        filas = con.execute(sql, params).fetchall()
    return [{
        "id": f[0], "titulo": f[1], "categoria": f[2], "puntuacion": f[3],
        "comentario": f[4] or "", "favorito": bool(f[5]), "fecha": f[6],
        "autor": f[7], "publica": bool(f[8])
    } for f in filas]
def obtener_listas():
    with conectar() as con:
        listas_db = con.execute(
            "SELECT id, nombre FROM listas WHERE autor = ? ORDER BY id DESC", (usuario_actual,)
        ).fetchall()
        return [{
            "nombre": nombre,
            "elementos": [r[0] for r in con.execute(
                "SELECT titulo_elemento FROM elementos_lista WHERE lista_id = ?", (lista_id,)
            ).fetchall()]
        } for lista_id, nombre in listas_db]
def limpiar():
    for elemento in contenido.winfo_children():
        elemento.destroy()
def titulo_pagina(texto):
    ctk.CTkLabel(contenido, text=texto, font=("Arial", 24, "bold"),
                 text_color="#8055A0").pack(pady=(18, 8))
def boton(parent, texto, comando, color=COLOR_LILA, **kwargs):
    # Personalizar hover_color desde cada botón sin duplicar el código.
    color_hover = kwargs.pop("hover_color", COLOR_LILA_HOVER)
    return ctk.CTkButton(parent, text=texto, command=comando, fg_color=color,
                         hover_color=color_hover, **kwargs)
def estrellas(puntuacion):
    return "★" * int(puntuacion) + "☆" * (5 - int(puntuacion))
def hash_contrasena(texto):
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()
def abrir_sesion():
    limpiar()
    titulo_pagina("¡Bienvenida/o a FanFrame!")
    ctk.CTkLabel(contenido, text="Elegí cómo querés entrar y el nombre que se mostrará en la comunidad.",
                 wraplength=560).pack(pady=6)
    modo_var = ctk.StringVar(value="Espectador")
    ctk.CTkSegmentedButton(contenido, values=["Espectador", "Editor"], variable=modo_var).pack(pady=10)
    nombre = ctk.CTkEntry(contenido, placeholder_text="Tu nombre o seudónimo", width=320)
    nombre.pack(pady=8)
    with conectar() as con:
        fila = con.execute("SELECT valor FROM ajustes WHERE clave='ultimo_editor'").fetchone()
    if fila:
        nombre.insert(0, fila[0])
    def entrar():
        global usuario_actual, modo_actual
        elegido = nombre.get().strip()
        if not elegido:
            messagebox.showwarning("Falta el nombre", "Escribí un nombre para continuar.")
            return
        elegido_modo = modo_var.get()
        if elegido_modo == "Editor":
            with conectar() as con:
                guardada = con.execute("SELECT valor FROM ajustes WHERE clave='contrasena_editor'").fetchone()
            if not guardada:
                primera = simpledialog.askstring("Crear contraseña de editor", "Creá una contraseña para proteger el acceso de editor:", show="*", parent=app)
                if not primera:
                    return
                repetir = simpledialog.askstring("Confirmar contraseña", "Volvé a escribir la contraseña:", show="*", parent=app)
                if primera != repetir:
                    messagebox.showerror("No coincide", "Las contraseñas no coinciden.")
                    return
                if len(primera) < 4:
                    messagebox.showwarning("Contraseña muy corta", "Usá al menos 4 caracteres.")
                    return
                with conectar() as con:
                    con.execute("INSERT OR REPLACE INTO ajustes(clave, valor) VALUES('contrasena_editor', ?)", (hash_contrasena(primera),))
            else:
                clave = simpledialog.askstring("Contraseña de editor", "Ingresá la contraseña de editor:", show="*", parent=app)
                if clave is None or hash_contrasena(clave) != guardada[0]:
                    messagebox.showerror("Acceso denegado", "La contraseña es incorrecta.")
                    return
            with conectar() as con:
                con.execute("INSERT OR REPLACE INTO ajustes(clave, valor) VALUES('ultimo_editor', ?)", (elegido,))
        usuario_actual = elegido
        modo_actual = elegido_modo
        construir_barra()
        inicio()
    boton(contenido, "Ingresar", entrar, width=180).pack(pady=14)
    ctk.CTkLabel(contenido, text="La primera vez que ingreses como editor, crearás una contraseña.",
                 text_color="#776A82", wraplength=500).pack(pady=4)
def construir_barra():
    contenido.pack_forget()
    barra.pack(fill="x", padx=10, pady=10, side="top")
    contenido.pack(fill="both", expand=True, padx=10, pady=5, side="top")
    for widget in barra.winfo_children():
        widget.destroy()
    if modo_actual == "Editor" and not vista_previa_espectador:
        ctk.CTkLabel(barra, text=f"{usuario_actual} · EDITOR",
                     text_color=COLOR_TEXTO, font=("Arial", 13, "bold")).pack(side="left", padx=10)
        boton(barra, "Panel del editor ▾", alternar_panel_editor, color=COLOR_ROSA,
              height=32, width=145).pack(side="left", padx=5, pady=7)
        boton(barra, "App (vista espectador)", mostrar_app_espectador, color=COLOR_CELESTE,
              text_color=COLOR_TEXTO, hover_color="#C8E4F5", height=32, width=165).pack(side="left", padx=5, pady=7)
    else:
        etiqueta = "Espectador (vista previa)" if modo_actual == "Editor" else "Espectador"
        ctk.CTkLabel(barra, text=f"{usuario_actual} · {etiqueta}",
                     text_color=COLOR_TEXTO, font=("Arial", 13, "bold")).pack(side="left", padx=8)
        opciones = [
            ("Inicio", inicio, COLOR_LILA), ("Buscar", buscar_para_resenar, COLOR_LILA),
            ("Recomendaciones", ver_recomendaciones, COLOR_ROSA), ("Mis reseñas", ver_mis_resenas, COLOR_LILA),
            ("Comunidad", ver_comunidad, COLOR_ROSA), ("Favoritos", ver_favoritos, COLOR_LILA),
            ("Crear lista", crear_lista, COLOR_ROSA), ("Mis listas", ver_listas, COLOR_LILA),
            ("Perfil y estadísticas", ver_perfil, COLOR_ROSA),
        ]
        for texto, comando, color in opciones:
            ctk.CTkButton(barra, text=texto, command=comando, fg_color=color,
                          hover_color=COLOR_LILA_HOVER, height=30, width=105).pack(side="left", padx=3, pady=7)
        if modo_actual == "Editor":
            boton(barra, "Volver al editor", volver_a_vista_editor, color=COLOR_ROSA,
                  height=30, width=130).pack(side="left", padx=4, pady=7)
    ctk.CTkButton(barra, text="Cerrar sesión", command=cerrar_sesion,
                  fg_color="#8B8791", hover_color="#6F6B75", height=30).pack(side="right", padx=7)
def mostrar_app_espectador():
    """Activa una vista de comprobación igual a la navegación del espectador, sin controles de editor."""
    global vista_previa_espectador
    if modo_actual != "Editor":
        return
    vista_previa_espectador = True
    construir_barra()
    inicio()
def volver_a_vista_editor():
    """Sale de la vista previa y vuelve a mostrar las herramientas del editor."""
    global vista_previa_espectador
    vista_previa_espectador = False
    construir_barra()
    alternar_panel_editor()
def alternar_panel_editor():
    global vista_previa_espectador
    if modo_actual != "Editor":
        messagebox.showerror("Acceso restringido", "Solo el editor puede abrir este panel.")
        return
    vista_previa_espectador = False
    construir_barra()
    limpiar()
    titulo_pagina("Panel del editor")
    ctk.CTkLabel(contenido, text="Las herramientas aparecen solo cuando abrís este panel.",
                 wraplength=560).pack(pady=8)
    boton(contenido, "Revisar reseñas de la comunidad", ver_comunidad, width=300).pack(pady=5)
    boton(contenido, "Revisar propuestas pendientes", ver_propuestas, color=COLOR_ROSA, width=300).pack(pady=5)
    boton(contenido, "Ver catálogo actual", ver_catalogo, width=300).pack(pady=5)
    boton(contenido, "Volver al inicio", inicio, color=COLOR_ROSA, width=300).pack(pady=12)
def crear_tarjeta_catalogo(parent, item):
    """Construye una tarjeta de catálogo reutilizable."""
    tarjeta = ctk.CTkFrame(parent, fg_color=COLOR_TARJETA, corner_radius=8)
    tarjeta.pack(fill="x", padx=20, pady=4)
    ctk.CTkLabel(
        tarjeta,
        text=f"{item['titulo']} · {item['categoria']}",
        font=("Arial", 13, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w",
    ).pack(fill="x", padx=10, pady=(7, 2))
    ctk.CTkLabel(
        tarjeta,
        text=item.get("descripcion", ""),
        text_color=COLOR_TEXTO,
        wraplength=540,
        justify="left",
        anchor="w",
    ).pack(fill="x", padx=10, pady=(0, 8))
def ver_catalogo():
    if modo_actual != "Editor":
        messagebox.showerror("Acceso restringido", "Solo el editor puede revisar el catálogo.")
        return
    limpiar()
    titulo_pagina("Catálogo actual")
    for item in CATALOGO:
        crear_tarjeta_catalogo(contenido, item)
def cerrar_sesion():
    global usuario_actual, modo_actual, vista_previa_espectador
    if not messagebox.askyesno("Cerrar sesión", "¿Querés cerrar la sesión actual?"):
        return
    usuario_actual = ""
    modo_actual = "Espectador"
    vista_previa_espectador = False
    for widget in barra.winfo_children():
        widget.destroy()
    barra.pack_forget()
    abrir_sesion()
def inicio():
    limpiar()
    titulo_pagina("FanFrame")
    ctk.CTkLabel(contenido,
        text="Registrá y compartí tus películas, series, canciones, álbumes, artistas y libros favoritos.",
        wraplength=560).pack(pady=8)
    propias = obtener_resenas(autor=usuario_actual)
    publicas = obtener_resenas(publicas=True)
    ctk.CTkLabel(contenido,
        text=f"Mis reseñas: {len(propias)}   ·   Reseñas públicas: {len(publicas)}",
        font=("Arial", 15, "bold"), text_color="#8055A0").pack(pady=8)
    ctk.CTkLabel(contenido, text="¿No sabés qué reseñar? Probá alguna recomendación:",
                 text_color="#776A82").pack(pady=(14, 5))
    for titulo, categoria, motivo in RECOMENDACIONES[:4]:
        tarjeta = ctk.CTkFrame(contenido, fg_color=COLOR_TARJETA, corner_radius=10)
        tarjeta.pack(fill="x", padx=25, pady=5)
        ctk.CTkLabel(tarjeta, text=f"{titulo} · {categoria}",
                     font=("Arial", 14, "bold"), text_color=COLOR_TEXTO).pack(anchor="w", padx=12, pady=(8, 1))
        ctk.CTkLabel(tarjeta, text=motivo, text_color="#776A82",
                     wraplength=500, justify="left").pack(anchor="w", padx=12, pady=(0, 5))
        boton(tarjeta, "Reseñar", lambda t=titulo, c=categoria: agregar_resena({"titulo": t, "categoria": c}),
              width=90, height=28).pack(anchor="e", padx=10, pady=(0, 8))
def buscar_para_resenar():
    """Buscador con sugerencias predictivas basadas en catálogo e historial."""
    import difflib
    import unicodedata

    limpiar()
    titulo_pagina("Buscador cultural")
    ctk.CTkLabel(
        contenido,
        text="Empezá a escribir: FanFrame te sugerirá títulos y búsquedas frecuentes.",
        wraplength=560
    ).pack(pady=(0, 10))

    buscador = ctk.CTkEntry(
        contenido,
        placeholder_text="Ej.: Taylor Swift, Los Simuladores, El Señor de los Anillos...",
        width=430,
        height=38
    )
    buscador.pack(pady=5)

    estado_sugerencias = ctk.CTkLabel(
        contenido, text="Tendencias y búsquedas recientes", text_color="#776A82"
    )
    estado_sugerencias.pack(pady=(4, 0))

    sugerencias = ctk.CTkFrame(contenido, fg_color="transparent")
    sugerencias.pack(fill="x", padx=15, pady=3)

    resultados = ctk.CTkFrame(contenido, fg_color="transparent")
    resultados.pack(fill="both", expand=True, padx=10, pady=8)

    def normalizar(texto):
        texto = unicodedata.normalize("NFKD", str(texto))
        texto = "".join(c for c in texto if not unicodedata.combining(c))
        return texto.casefold().strip()

    def obtener_fuentes_sugerencias():
        """Reúne títulos, recomendaciones y búsquedas guardadas en SQLite."""
        fuentes = {}

        for item in CATALOGO:
            titulo = item.get("titulo", "").strip()
            if titulo:
                fuentes.setdefault(titulo, {
                    "categoria": item.get("categoria", "Contenido"),
                    "origen": "Catálogo",
                    "popularidad": 0
                })

        for titulo, categoria, _motivo in RECOMENDACIONES:
            fuentes.setdefault(titulo, {
                "categoria": categoria,
                "origen": "Recomendación",
                "popularidad": 0
            })

        for resena in obtener_resenas():
            titulo = resena.get("titulo", "").strip()
            if titulo:
                fuentes.setdefault(titulo, {
                    "categoria": resena.get("categoria", "Contenido"),
                    "origen": "Reseñas",
                    "popularidad": 0
                })

        with conectar() as con:
            populares = con.execute("""
                SELECT consulta,
                       COUNT(*) AS cantidad,
                       SUM(CASE WHEN autor = ? THEN 3 ELSE 1 END) AS relevancia_personal,
                       MAX(id) AS mas_reciente
                FROM busquedas
                WHERE trim(consulta) <> ''
                GROUP BY lower(trim(consulta))
                ORDER BY relevancia_personal DESC, cantidad DESC, mas_reciente DESC
                LIMIT 100
            """, (usuario_actual,)).fetchall()

        for consulta, cantidad, relevancia_personal, _reciente in populares:
            consulta = consulta.strip()
            if not consulta:
                continue
            clave = next(
                (titulo for titulo in fuentes
                 if normalizar(titulo) == normalizar(consulta)),
                consulta
            )
            actual = fuentes.get(clave, {})
            fuentes[clave] = {
                "categoria": actual.get("categoria", "Búsqueda frecuente"),
                "origen": "Búsqueda frecuente",
                "popularidad": int(cantidad or 0) + int(relevancia_personal or 0)
            }

        return fuentes

    def obtener_sugerencias(texto):
        fuentes = obtener_fuentes_sugerencias()
        consulta = normalizar(texto)
        puntuadas = []

        for titulo, datos in fuentes.items():
            nombre = normalizar(titulo)
            puntuacion = 0

            if not consulta:
                # En el campo vacío se priorizan búsquedas populares.
                puntuacion += datos.get("popularidad", 0) * 4
                if datos.get("origen") == "Recomendación":
                    puntuacion += 2
            elif nombre.startswith(consulta):
                puntuacion += 100
            elif any(palabra.startswith(consulta) for palabra in nombre.split()):
                puntuacion += 75
            elif consulta in nombre:
                puntuacion += 55
            else:
                similitud = difflib.SequenceMatcher(None, consulta, nombre).ratio()
                palabras_similares = max(
                    (difflib.SequenceMatcher(None, consulta, palabra).ratio()
                     for palabra in nombre.split()),
                    default=0
                )
                if similitud >= 0.38:
                    puntuacion += int(similitud * 40)
                if palabras_similares >= 0.60:
                    puntuacion += int(palabras_similares * 35)

            if consulta and puntuacion:
                puntuacion += min(datos.get("popularidad", 0), 15)

            if puntuacion > 0:
                puntuadas.append((puntuacion, titulo, datos))

        puntuadas.sort(
            key=lambda elemento: (
                -elemento[0],
                normalizar(elemento[1])
            )
        )
        return puntuadas[:8]

    def elegir_sugerencia(titulo):
        buscador.delete(0, "end")
        buscador.insert(0, titulo)
        realizar_busqueda()

    def actualizar_sugerencias(event=None):
        # No ejecutar la búsqueda al presionar Enter; ese evento lo atiende
        # realizar_busqueda para evitar guardar dos veces la misma consulta.
        for widget in sugerencias.winfo_children():
            widget.destroy()

        texto = buscador.get().strip()
        sugeridas = obtener_sugerencias(texto)

        estado_sugerencias.configure(
            text="Sugerencias para tu búsqueda" if texto
            else "Tendencias y búsquedas frecuentes"
        )

        if not sugeridas:
            ctk.CTkLabel(
                sugerencias,
                text="Todavía no encontramos coincidencias. Probá con otra palabra.",
                text_color="#776A82"
            ).pack(anchor="w", pady=4)
            return

        for _puntuacion, titulo, datos in sugeridas:
            categoria = datos.get("categoria", "Contenido")
            origen = datos.get("origen", "Catálogo")
            texto_boton = f"{titulo}  ·  {categoria}"
            if origen == "Búsqueda frecuente":
                texto_boton += "  ·  frecuente"

            ctk.CTkButton(
                sugerencias,
                text=texto_boton,
                anchor="w",
                fg_color=COLOR_CELESTE,
                text_color=COLOR_TEXTO,
                hover_color="#C8E4F5",
                command=lambda t=titulo: elegir_sugerencia(t)
            ).pack(fill="x", pady=2)

    def realizar_busqueda(event=None):
        consulta = buscador.get().strip()
        if not consulta:
            return "break" if event else None

        with conectar() as con:
            con.execute(
                "INSERT INTO busquedas(consulta, autor, fecha) VALUES(?,?,?)",
                (
                    consulta,
                    usuario_actual,
                    datetime.now().isoformat(timespec="seconds")
                )
            )

        for widget in resultados.winfo_children():
            widget.destroy()

        consulta_normalizada = normalizar(consulta)
        encontrados = [
            item for item in CATALOGO
            if consulta_normalizada in normalizar(item.get("titulo", ""))
        ]
        conocidos = {normalizar(item["titulo"]) for item in encontrados}

        for resena in obtener_resenas():
            titulo = resena.get("titulo", "")
            clave = normalizar(titulo)
            if consulta_normalizada in clave and clave not in conocidos:
                encontrados.append({
                    "titulo": titulo,
                    "categoria": resena.get("categoria", "Contenido"),
                    "descripcion": "Contenido encontrado en las reseñas de FanFrame."
                })
                conocidos.add(clave)

        if encontrados:
            ctk.CTkLabel(
                resultados,
                text=f"Resultados: {len(encontrados)}",
                font=("Arial", 14, "bold"),
                text_color="#8055A0"
            ).pack(anchor="w")

            for item in encontrados:
                tarjeta = ctk.CTkFrame(
                    resultados, fg_color=COLOR_TARJETA, corner_radius=9
                )
                tarjeta.pack(fill="x", pady=4)

                info = ctk.CTkFrame(tarjeta, fg_color="transparent")
                info.pack(side="left", fill="x", expand=True, padx=12, pady=7)

                ctk.CTkLabel(
                    info,
                    text=f"{item['titulo']} · {item['categoria']}",
                    font=("Arial", 13, "bold"),
                    text_color=COLOR_TEXTO,
                    anchor="w"
                ).pack(fill="x")

                descripcion = item.get(
                    "descripcion",
                    "Podés crear una reseña sobre este elemento."
                )
                ctk.CTkLabel(
                    info,
                    text=descripcion,
                    text_color=COLOR_TEXTO,
                    wraplength=390,
                    justify="left",
                    anchor="w"
                ).pack(fill="x", pady=(2, 0))

                boton(
                    tarjeta,
                    "Reseñar",
                    lambda x=item: agregar_resena(x),
                    width=90
                ).pack(side="right", padx=8, pady=6)
        else:
            ctk.CTkLabel(
                resultados,
                text=(
                    "No aparece en el catálogo. Podés enviar una propuesta "
                    "para que el editor la revise."
                ),
                wraplength=500
            ).pack(pady=8)

            boton(
                resultados,
                "Enviar propuesta",
                lambda: enviar_propuesta(consulta),
                color=COLOR_ROSA
            ).pack(pady=5)

            boton(
                resultados,
                "Crear reseña igualmente",
                lambda: agregar_resena({
                    "titulo": consulta,
                    "categoria": "Otro"
                })
            ).pack(pady=5)

        actualizar_sugerencias()
        return "break" if event else None

    buscador.bind("<KeyRelease>", actualizar_sugerencias)
    buscador.bind("<Return>", realizar_busqueda)
    boton(contenido, "Buscar", realizar_busqueda).pack(pady=5)
    boton(
        contenido,
        "Ver recomendaciones",
        ver_recomendaciones,
        color=COLOR_ROSA
    ).pack(pady=(3, 10))

    # Mostrar tendencias desde el momento en que se abre el buscador.
    actualizar_sugerencias()

def enviar_propuesta(titulo):
    titulo = titulo.strip()
    if not titulo:
        return
    categoria = simpledialog.askstring("Categoría", "¿Qué tipo de contenido es? (Película, Serie, Canción, Álbum, Artista, Libro u Otro)", parent=app)
    if not categoria:
        return
    categoria = categoria.strip().title()
    if categoria not in CATEGORIAS:
        categoria = "Otro"
    with conectar() as con:
        duplicada = con.execute("SELECT id FROM propuestas WHERE lower(titulo)=lower(?) AND estado='Pendiente'", (titulo,)).fetchone()
        if duplicada:
            messagebox.showinfo("Propuesta existente", "Ese título ya está pendiente de revisión.")
            return
        con.execute("INSERT INTO propuestas(titulo,categoria,autor,fecha,estado) VALUES(?,?,?,?,?)",
                    (titulo, categoria, usuario_actual, date.today().isoformat(), "Pendiente"))
    messagebox.showinfo("Propuesta enviada", "El editor podrá aceptarla o denegarla desde su panel.")
def ver_propuestas():
    if modo_actual != "Editor":
        messagebox.showerror("Acceso restringido", "Solo el editor puede gestionar propuestas.")
        return
    limpiar()
    titulo_pagina("Propuestas de espectadores")
    with conectar() as con:
        propuestas = con.execute("SELECT id,titulo,categoria,autor,fecha FROM propuestas WHERE estado='Pendiente' ORDER BY id DESC").fetchall()
    if not propuestas:
        ctk.CTkLabel(contenido, text="No hay propuestas pendientes.").pack(pady=10)
    for pid, titulo, categoria, autor, fecha in propuestas:
        tarjeta = ctk.CTkFrame(contenido, fg_color=COLOR_TARJETA, corner_radius=10)
        tarjeta.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(tarjeta, text=f"{titulo} · {categoria}", font=("Arial", 14, "bold"),
                     text_color=COLOR_TEXTO).pack(anchor="w", padx=12, pady=(8, 2))
        ctk.CTkLabel(tarjeta, text=f"Propuesta de {autor} · {fecha}", text_color="#776A82").pack(anchor="w", padx=12, pady=(0, 6))
        fila = ctk.CTkFrame(tarjeta, fg_color="transparent")
        fila.pack(anchor="e", padx=8, pady=(0, 8))
        def aceptar(propuesta_id=pid, t=titulo, c=categoria):
            with conectar() as con:
                con.execute("UPDATE propuestas SET estado='Aceptada' WHERE id=?", (propuesta_id,))
                con.execute("INSERT OR IGNORE INTO catalogo_aprobado(titulo,categoria) VALUES(?,?)", (t, c))
            if not any(x["titulo"].casefold() == t.casefold() and x["categoria"] == c for x in CATALOGO):
                CATALOGO.append({"titulo": t, "categoria": c})
            messagebox.showinfo("Propuesta aceptada", f"“{t}” se agregó al catálogo y quedará guardado.")
            ver_propuestas()
        def denegar(propuesta_id=pid):
            with conectar() as con:
                con.execute("UPDATE propuestas SET estado='Denegada' WHERE id=?", (propuesta_id,))
            ver_propuestas()
        boton(fila, "Aceptar", aceptar, width=90).pack(side="left", padx=4)
        boton(fila, "Denegar", denegar, color="#C85B83", width=90).pack(side="left", padx=4)
def ver_recomendaciones():
    limpiar()
    titulo_pagina("Recomendaciones para reseñar")
    for titulo, categoria, motivo in RECOMENDACIONES:
        tarjeta = ctk.CTkFrame(contenido, fg_color=COLOR_TARJETA, corner_radius=10)
        tarjeta.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(tarjeta, text=f"{titulo} · {categoria}",
                     font=("Arial", 14, "bold"), text_color=COLOR_TEXTO).pack(anchor="w", padx=12, pady=(8, 1))
        ctk.CTkLabel(tarjeta, text=motivo, text_color="#776A82",
                     wraplength=520, justify="left").pack(anchor="w", padx=12, pady=(0, 5))
        boton(tarjeta, "Reseñar", lambda t=titulo, c=categoria: agregar_resena({"titulo": t, "categoria": c}),
              width=90, height=28).pack(anchor="e", padx=10, pady=(0, 8))
def agregar_resena(item=None, resena_id=None):
    existente = None
    if resena_id is not None:
        propias = [r for r in obtener_resenas(autor=usuario_actual) if r["id"] == resena_id]
        if not propias:
            messagebox.showerror("Sin permiso", "Solo podés editar tus propias reseñas.")
            return
        existente = propias[0]
    limpiar()
    titulo_pagina("Editar reseña" if existente else "Agregar reseña")
    formulario = ctk.CTkFrame(contenido, fg_color=COLOR_TARJETA, corner_radius=12)
    formulario.pack(fill="x", padx=20, pady=8)
    ctk.CTkLabel(formulario, text="Título").pack(anchor="w", padx=15, pady=(12, 3))
    campo_titulo = ctk.CTkEntry(formulario, placeholder_text="Nombre del contenido")
    campo_titulo.pack(anchor="w", padx=15, fill="x")
    ctk.CTkLabel(formulario, text="Categoría").pack(anchor="w", padx=15, pady=(10, 3))
    cat_menu = ctk.CTkOptionMenu(formulario, values=CATEGORIAS, fg_color=COLOR_LILA, button_color=COLOR_LILA_HOVER)
    cat_menu.pack(anchor="w", padx=15)
    ctk.CTkLabel(formulario, text="Puntuación").pack(anchor="w", padx=15, pady=(10, 3))
    puntuacion = ctk.CTkOptionMenu(formulario, values=["1", "2", "3", "4", "5"],
                                  fg_color=COLOR_LILA, button_color=COLOR_LILA_HOVER)
    puntuacion.set("5")
    puntuacion.pack(anchor="w", padx=15)
    ctk.CTkLabel(formulario, text="Tu opinión").pack(anchor="w", padx=15, pady=(10, 3))
    comentario = ctk.CTkTextbox(formulario, height=110, fg_color="#FFFCFF", text_color=COLOR_TEXTO)
    comentario.pack(fill="x", padx=15)
    favorito = ctk.CTkCheckBox(formulario, text="Es mi favorito", text_color=COLOR_TEXTO,
                               fg_color=COLOR_LILA, hover_color=COLOR_LILA_HOVER)
    favorito.pack(anchor="w", padx=15, pady=10)
    publica = ctk.CTkCheckBox(formulario, text="Publicar en la comunidad", text_color=COLOR_TEXTO,
                              fg_color=COLOR_ROSA, hover_color=COLOR_ROSA_HOVER)
    publica.pack(anchor="w", padx=15, pady=(0, 12))
    if existente:
        campo_titulo.insert(0, existente["titulo"])
        cat_menu.set(existente["categoria"] if existente["categoria"] in CATEGORIAS else "Otro")
        puntuacion.set(str(existente["puntuacion"]))
        comentario.insert("1.0", existente["comentario"])
        if existente["favorito"]:
            favorito.select()
        if existente["publica"]:
            publica.select()
    elif item:
        campo_titulo.insert(0, item.get("titulo", ""))
        cat_menu.set(item.get("categoria", "Otro") if item.get("categoria", "Otro") in CATEGORIAS else "Otro")
        publica.select()
    def guardar():
        nombre = campo_titulo.get().strip()
        if not nombre:
            messagebox.showwarning("Falta el título", "Ingresá un título.")
            return
        valores = (nombre, cat_menu.get(), int(puntuacion.get()),
                   comentario.get("1.0", "end").strip(), 1 if favorito.get() else 0,
                   date.today().isoformat(), 1 if publica.get() else 0)
        try:
            with conectar() as con:
                if existente:
                    con.execute("""UPDATE resenas SET titulo=?, categoria=?, puntuacion=?, comentario=?,
                                   favorito=?, fecha=?, publica=? WHERE id=? AND autor=?""",
                                valores[:6] + (valores[6], resena_id, usuario_actual))
                else:
                    con.execute("""INSERT INTO resenas
                        (titulo,categoria,puntuacion,comentario,favorito,fecha,autor,publica)
                        VALUES(?,?,?,?,?,?,?,?)""",
                        (valores[0], valores[1], valores[2], valores[3], valores[4],
                         valores[5], usuario_actual, valores[6]))
            messagebox.showinfo("Guardado", "La reseña se guardó correctamente.")
            ver_mis_resenas()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo guardar la reseña:\n{e}")
    boton(formulario, "Guardar cambios" if existente else "Guardar reseña", guardar,
          color=COLOR_LILA_HOVER).pack(anchor="w", padx=15, pady=(0, 12))
    boton(contenido, "Volver a mis reseñas", ver_mis_resenas, color=COLOR_ROSA).pack(pady=8)
def eliminar_resena(resena_id):
    if not messagebox.askyesno("Eliminar reseña", "¿Seguro que querés eliminar esta reseña? También se borrarán sus comentarios y reacciones."):
        return
    with conectar() as con:
        con.execute("DELETE FROM resenas WHERE id=? AND autor=?", (resena_id, usuario_actual))
    ver_mis_resenas()
def tarjeta_resena(parent, r, permitir_editar=False, comunidad=False):
    tarjeta = ctk.CTkFrame(parent, fg_color=COLOR_CELESTE if comunidad else COLOR_TARJETA, corner_radius=10)
    tarjeta.pack(fill="x", padx=12, pady=6)
    fav = " · ❤️ Favorito" if r["favorito"] else ""
    ctk.CTkLabel(tarjeta, text=f"{r['titulo']} · {r['categoria']}",
                 font=("Arial", 15, "bold"), text_color=COLOR_TEXTO,
                 wraplength=620).pack(anchor="w", padx=12, pady=(10, 2))
    ctk.CTkLabel(tarjeta, text=f"Por {r['autor']} · {estrellas(r['puntuacion'])}{fav} · {r['fecha']}",
                 text_color="#776A82").pack(anchor="w", padx=12)
    ctk.CTkLabel(tarjeta, text=r["comentario"] or "Sin comentario",
                 text_color=COLOR_TEXTO, justify="left", wraplength=620).pack(anchor="w", padx=12, pady=7)
    if comunidad:
        with conectar() as con:
            likes = con.execute("SELECT COUNT(*) FROM reacciones WHERE resena_id=?", (r["id"],)).fetchone()[0]
            reaccion = con.execute("SELECT 1 FROM reacciones WHERE resena_id=? AND autor=?",
                                   (r["id"], usuario_actual)).fetchone()
            cantidad_comentarios = con.execute("SELECT COUNT(*) FROM comentarios WHERE resena_id=?", (r["id"],)).fetchone()[0]
        fila = ctk.CTkFrame(tarjeta, fg_color="transparent")
        fila.pack(fill="x", padx=8, pady=(0, 8))
        boton(fila, f"❤️ Me gusta ({likes})" if not reaccion else f"💗 Te gusta ({likes})",
              lambda rid=r["id"]: alternar_reaccion(rid), color=COLOR_ROSA, width=140).pack(side="left", padx=3)
        boton(fila, f"Comentarios ({cantidad_comentarios})",
              lambda rid=r["id"]: ver_comentarios(rid), color=COLOR_LILA, width=130).pack(side="left", padx=3)
        if r["autor"] == usuario_actual:
            boton(fila, "Editar", lambda rid=r["id"]: agregar_resena(resena_id=rid), width=75).pack(side="right", padx=3)
    if permitir_editar:
        fila = ctk.CTkFrame(tarjeta, fg_color="transparent")
        fila.pack(fill="x", padx=8, pady=(0, 8))
        boton(fila, "Editar", lambda rid=r["id"]: agregar_resena(resena_id=rid), width=90).pack(side="left", padx=3)
        boton(fila, "Eliminar", lambda rid=r["id"]: eliminar_resena(rid),
              color="#C85B83", width=90).pack(side="left", padx=3)
def ver_mis_resenas():
    limpiar()
    titulo_pagina("Mis reseñas")
    ctk.CTkLabel(contenido, text="Tus reseñas personales. Podés editarlas o eliminarlas.",
                 text_color="#776A82").pack(pady=(0, 8))
    resenas = obtener_resenas(autor=usuario_actual)
    if not resenas:
        ctk.CTkLabel(contenido, text="Todavía no tenés reseñas.").pack(pady=10)
        boton(contenido, "Crear una reseña", agregar_resena).pack(pady=5)
        return
    for r in resenas:
        tarjeta_resena(contenido, r, permitir_editar=True)
def ver_favoritos():
    limpiar()
    titulo_pagina("Mis favoritos")
    favoritos = obtener_resenas(autor=usuario_actual, solo_favoritos=True)
    if not favoritos:
        ctk.CTkLabel(contenido, text="Todavía no marcaste reseñas como favoritas.").pack(pady=10)
        return
    for r in favoritos:
        tarjeta_resena(contenido, r, permitir_editar=True)
def ver_comunidad():
    limpiar()
    titulo_pagina("Reseñas de la comunidad")
    ctk.CTkLabel(contenido, text="Reseñas que sus autores eligieron publicar en esta instalación.",
                 text_color="#776A82", wraplength=560).pack(pady=(0, 8))
    # Filtro para alternar la vista pública y las reseñas propias.
    tabs = ctk.CTkFrame(contenido, fg_color="transparent")
    tabs.pack(fill="x", padx=12)
    boton(tabs, "Reseñas de la comunidad", ver_comunidad, color=COLOR_ROSA).pack(side="left", padx=3)
    boton(tabs, "Mis propias reseñas", ver_mis_resenas, color=COLOR_LILA).pack(side="left", padx=3)
    resenas = obtener_resenas(publicas=True)
    if not resenas:
        ctk.CTkLabel(contenido, text="Todavía no hay reseñas públicas.").pack(pady=10)
        return
    for r in resenas:
        tarjeta_resena(contenido, r, comunidad=True)
def alternar_reaccion(resena_id):
    with conectar() as con:
        existe = con.execute("SELECT id FROM reacciones WHERE resena_id=? AND autor=?",
                             (resena_id, usuario_actual)).fetchone()
        if existe:
            con.execute("DELETE FROM reacciones WHERE resena_id=? AND autor=?", (resena_id, usuario_actual))
        else:
            con.execute("INSERT OR IGNORE INTO reacciones(resena_id, autor, tipo) VALUES(?,?,?)",
                        (resena_id, usuario_actual, "❤️"))
    ver_comunidad()
def ver_comentarios(resena_id):
    limpiar()
    titulo_pagina("Comentarios y respuestas")
    with conectar() as con:
        comentarios = con.execute("""
            SELECT id, autor, texto, fecha, respuesta_a
            FROM comentarios WHERE resena_id=? ORDER BY id
        """, (resena_id,)).fetchall()
    raiz = ctk.CTkFrame(contenido, fg_color="transparent")
    raiz.pack(fill="both", expand=True, padx=12)
    if not comentarios:
        ctk.CTkLabel(raiz, text="Todavía no hay comentarios.").pack(pady=8)
    for cid, autor, texto, fecha, respuesta_a in comentarios:
        prefijo = "↳ " if respuesta_a else ""
        ctk.CTkLabel(raiz, text=f"{prefijo}{autor} · {fecha}\n{texto}",
                     justify="left", anchor="w", fg_color=COLOR_TARJETA,
                     corner_radius=8, text_color=COLOR_TEXTO,
                     wraplength=600).pack(fill="x", pady=4, ipady=7, padx=4)
        boton(raiz, f"Responder a {autor}", lambda c=cid, a=autor: responder_comentario(resena_id, c, a),
              color=COLOR_ROSA, height=26).pack(anchor="e", padx=5, pady=(0, 5))
    ctk.CTkLabel(raiz, text="Escribí un comentario").pack(anchor="w", pady=(10, 3))
    campo = ctk.CTkTextbox(raiz, height=80)
    campo.pack(fill="x", pady=4)
    def publicar():
        texto = campo.get("1.0", "end").strip()
        if not texto:
            messagebox.showwarning("Comentario vacío", "Escribí algo antes de publicar.")
            return
        with conectar() as con:
            con.execute("INSERT INTO comentarios(resena_id, autor, texto, fecha) VALUES(?,?,?,?)",
                        (resena_id, usuario_actual, texto, date.today().isoformat()))
        ver_comentarios(resena_id)
    boton(raiz, "Publicar comentario", publicar).pack(anchor="w", pady=5)
    boton(raiz, "Volver a la comunidad", ver_comunidad, color=COLOR_ROSA).pack(anchor="w", pady=5)
def responder_comentario(resena_id, comentario_id, autor):
    texto = simpledialog.askstring("Responder", f"Tu respuesta a {autor}:", parent=app)
    if texto and texto.strip():
        with conectar() as con:
            con.execute("""INSERT INTO comentarios(resena_id, autor, texto, fecha, respuesta_a)
                           VALUES(?,?,?,?,?)""",
                        (resena_id, usuario_actual, texto.strip(), date.today().isoformat(), comentario_id))
        ver_comentarios(resena_id)
def crear_lista():
    limpiar()
    titulo_pagina("Crear lista cultural")
    nombre = ctk.CTkEntry(contenido, placeholder_text="Nombre de la lista", width=360)
    nombre.pack(pady=8)
    titulos = ctk.CTkEntry(contenido, placeholder_text="Títulos separados por coma", width=460)
    titulos.pack(pady=8)
    def guardar_lista():
        nombre_lista = nombre.get().strip()
        if not nombre_lista:
            messagebox.showwarning("Aviso", "Ingresá un nombre.")
            return
        elementos = [x.strip() for x in titulos.get().split(",") if x.strip()]
        with conectar() as con:
            cursor = con.execute("INSERT INTO listas(nombre, autor) VALUES(?,?)", (nombre_lista, usuario_actual))
            lista_id = cursor.lastrowid
            for elemento in elementos:
                con.execute("INSERT INTO elementos_lista(lista_id, titulo_elemento) VALUES(?,?)",
                            (lista_id, elemento))
        ver_listas()
    boton(contenido, "Guardar lista", guardar_lista, color=COLOR_ROSA).pack(pady=12)
def ver_listas():
    limpiar()
    titulo_pagina("Mis listas")
    listas = obtener_listas()
    if not listas:
        ctk.CTkLabel(contenido, text="Todavía no hay listas.").pack(pady=10)
        return
    for lista in listas:
        titulos = ", ".join(lista["elementos"]) or "Lista vacía"
        ctk.CTkLabel(contenido, text=f"{lista['nombre']}\n{titulos}",
                     fg_color=COLOR_CELESTE, corner_radius=8,
                     text_color=COLOR_TEXTO, wraplength=600).pack(fill="x", padx=20, pady=6, ipady=8)
def ver_perfil():
    limpiar()
    titulo_pagina(f"Perfil de {usuario_actual}")
    propias = obtener_resenas(autor=usuario_actual)
    favoritas = [r for r in propias if r["favorito"]]
    promedio = sum(r["puntuacion"] for r in propias) / len(propias) if propias else 0
    with conectar() as con:
        comentarios = con.execute("SELECT COUNT(*) FROM comentarios WHERE autor=?", (usuario_actual,)).fetchone()[0]
        reacciones = con.execute("SELECT COUNT(*) FROM reacciones WHERE autor=?", (usuario_actual,)).fetchone()[0]
        publicadas = con.execute("SELECT COUNT(*) FROM resenas WHERE autor=? AND publica=1", (usuario_actual,)).fetchone()[0]
        total_comunidad = con.execute("SELECT COUNT(*) FROM resenas WHERE publica=1").fetchone()[0]
        usuarios = con.execute("""
            SELECT COUNT(DISTINCT autor) FROM (
                SELECT autor FROM resenas WHERE publica=1
                UNION SELECT autor FROM comentarios
                UNION SELECT autor FROM reacciones
            )
        """).fetchone()[0]
        total_comentarios = con.execute("SELECT COUNT(*) FROM comentarios").fetchone()[0]
        total_reacciones = con.execute("SELECT COUNT(*) FROM reacciones").fetchone()[0]
    datos = [
        ("Reseñas propias", len(propias)),
        ("Reseñas públicas propias", publicadas),
        ("Favoritos", len(favoritas)),
        ("Puntuación promedio", f"{promedio:.1f} / 5"),
        ("Comentarios publicados", comentarios),
        ("Reacciones dadas", reacciones),
    ]
    for etiqueta, valor in datos:
        ctk.CTkLabel(contenido, text=f"{etiqueta}: {valor}",
                     fg_color=COLOR_TARJETA, text_color=COLOR_TEXTO,
                     corner_radius=8, anchor="w").pack(fill="x", padx=35, pady=4, ipady=7)
    ctk.CTkLabel(contenido, text="Estadísticas de la comunidad",
                 font=("Arial", 18, "bold"), text_color="#8055A0").pack(pady=(18, 7))
    for etiqueta, valor in [
        ("Usuarios con actividad", usuarios),
        ("Reseñas públicas", total_comunidad),
        ("Comentarios y respuestas", total_comentarios),
        ("Reacciones", total_reacciones),
    ]:
        ctk.CTkLabel(contenido, text=f"{etiqueta}: {valor}",
                     fg_color=COLOR_CELESTE, text_color=COLOR_TEXTO,
                     corner_radius=8, anchor="w").pack(fill="x", padx=35, pady=4, ipady=7)
    boton(contenido, "Cerrar sesión", cerrar_sesion, color=COLOR_ROSA).pack(pady=18)
# Aplicación principal
inicializar_bd()
with conectar() as con:
    aprobados = con.execute("SELECT titulo, categoria FROM catalogo_aprobado ORDER BY id").fetchall()
for titulo_aprobado, categoria_aprobada in aprobados:
    if not any(x["titulo"].casefold() == titulo_aprobado.casefold() and x["categoria"] == categoria_aprobada for x in CATALOGO):
        CATALOGO.append({"titulo": titulo_aprobado, "categoria": categoria_aprobada})
app = ctk.CTk()
app.title("FanFrame")
app.geometry("1120x760")
app.minsize(800, 600)
app.configure(fg_color=COLOR_FONDO)
barra = ctk.CTkFrame(app, fg_color=COLOR_TARJETA, corner_radius=12)

# La barra se mantiene creada, pero oculta hasta que el usuario ingrese.
contenido = ctk.CTkScrollableFrame(app, fg_color=COLOR_FONDO)
contenido.pack(fill="both", expand=True, padx=10, pady=5)
abrir_sesion()
app.mainloop()
