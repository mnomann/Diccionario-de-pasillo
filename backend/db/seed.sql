-- ============================================================================
-- DESENREDA - Datos Semilla
-- Modismos chilenos autenticos, culturalmente precisos
-- ============================================================================

-- 0. Limpieza (para re-ejecucion segura) ------------------------------------
TRUNCATE TABLE frase_palabra, sugerencia, frase, palabra, escenario, usuario RESTART IDENTITY CASCADE;

-- 1. Escenarios -------------------------------------------------------------
INSERT INTO escenario (nombre, descripcion, icono) VALUES
    ('Entrevista laboral',
     'Situaciones formales de busqueda de empleo donde el lenguaje coloquial puede causar confusion',
     'briefcase'),
    ('Medico',
     'Consultas y examenes medicos donde es importante describir sintomas con precision',
     'heart-pulse'),
    ('Amigos',
     'Conversaciones informales entre amigos donde abundan las muletillas y modismos',
     'people'),
    ('Trabajo',
     'Interacciones laborales cotidianas con companeros y jefes en ambiente informal',
     'building'),
    ('Familia',
     'Conversaciones familiares donde los modismos se usan con confianza y cariño',
     'house'),
    ('Fiesta / Carrete',
     'Eventos sociales y celebraciones donde el lenguaje es especialmente descontracturado',
     'party-popper');

-- 2. Palabras ---------------------------------------------------------------
INSERT INTO palabra (palabra, traduccion, categoria, nivel_formalidad, nivel_ironia, nivel_sarcasmo, pronunciacion_fonetica, ejemplo_uso, nota_cultural, origen, variantes) VALUES
    ('weon',
     'tonto, amigo o persona generica (segun contexto y tono)',
     'modismo',
     1, 3, 2,
     '/we.on/',
     'Oye weon, pasame la sal -> Oye amigo, pasame la sal / Deja de ser weon -> Deja de actuar tontamente',
     'Una de las palabras mas versatiles del castellano chileno. Puede ser insulto, saludo, muletilla o apelativo cariñoso segun el tono y contexto. Su significado cambia drasticamente con la entonacion.',
     'Del español "huevon", que originalmente describia a una persona perezosa. En Chile evoluciono hasta perder casi todo su sentido original.',
     '["hueon", "wn", "weon"]'::jsonb),

    ('pololo',
     'novio o pareja sentimental',
     'modismo',
     2, 0, 0,
     '/po.lo.lo/',
     'Voy a salir con mi pololo al cine -> Voy a salir con mi novio al cine',
     'Termino cariñoso y ampliamente aceptado en todos los estratos sociales. Tiene variante femenina "polola".',
     'Probablemente del mapudungun "pululu" (mosca que rodea la luz), describiendo metaforicamente a quien ronda a su pareja.',
     '["polola"]'::jsonb),

    ('bacán',
     'genial, excelente, muy bueno',
     'modismo',
     2, 1, 0,
     '/ba.kan/',
     'La fiesta estuvo bacan -> La fiesta estuvo genial',
     'Expresion positiva muy extendida. Aceptada incluso en contextos semiformal cuando se usa con mesura.',
     'Del lunfardo argentino "bacán", originalmente usado en el hampa portenio y luego popularizado en toda la region.',
     '["bacana", "bacano"]'::jsonb),

    ('cachai',
     '¿entiendes?, ¿comprendes?, ¿captas?',
     'muletilla',
     1, 1, 0,
     '/ka.tʃai/',
     'La cosa es asi, cachai, tenemos que terminar esto hoy -> La cosa es asi, ¿entiendes? tenemos que terminar esto hoy',
     'Muletilla omnipresente en el habla chilena. Funciona como verificador de comprension similar al "you know?" ingles.',
     'Conjugacion del verbo "cachar" (del ingles "to catch"), que significa entender o captar una idea.',
     '["cachay", "cachi"]'::jsonb),

    ('fome',
     'aburrido, insipido, sin gracia',
     'modismo',
     2, 2, 0,
     '/fo.me/',
     'La pelicula estuvo fome, mejor nos vamos -> La pelicula estuvo aburrida, mejor nos vamos',
     'Expresion que denota decepcion por algo que no cumplio expectativas. Muy usada entre jovenes y adultos.',
     'Posiblemente del calo espanol o del portugues "fome" (hambre), en el sentido de "dejar con hambre" de emocion.',
     '["fomeque"]'::jsonb),

    ('chato',
     'harto, cansado, hastiado de algo',
     'modismo',
     2, 1, 0,
     '/tʃa.to/',
     'Estoy chato de las pegas extras -> Estoy harto de los trabajos extras',
     'Literalmente "aplanado" o "sin relieve". La metafora es que la persona esta "aplanada" por la situacion.',
     'Del adjetivo "chato" (plano, sin elevacion). La expresion "estar chato" sugiere que la paciencia se ha agotado.',
     '["chata"]'::jsonb),

    ('pega',
     'trabajo, empleo, labor',
     'jerga',
     1, 0, 0,
     '/pe.ɣa/',
     'Encontre pega en una oficina nueva -> Encontre trabajo en una oficina nueva',
     'Termino omnipresente en el Chile laboral informal. Incluso profesionales usan "pega" en conversaciones cotidianas.',
     'Del verbo "pegar" (adherir, unir). Originalmente "pegarse a algo" como comprometerse con una tarea.',
     '["peguita"]'::jsonb),

    ('pololear',
     'andar de novios, tener una relacion sentimental formal',
     'modismo',
     2, 0, 0,
     '/po.lo.le.ar/',
     'Llevamos dos años pololeando -> Llevamos dos años de novios',
     'Etapa de relacion formal previa al compromiso matrimonial. Culturalmente distinto al "andar" o "tontear".',
     'Deriva de "pololo" (novio). El verbo describe la accion de mantener una relacion de pololeo.',
     '[]'::jsonb),

    ('carrete',
     'fiesta, parranda, celebracion social',
     'jerga',
     1, 0, 0,
     '/ka.re.te/',
     'Este sabado hay carrete en casa de la Maria -> Este sabado hay fiesta en casa de la Maria',
     'Designa cualquier reunion social con animacion, musica y usualmente alcohol. Actividad central de la vida social juvenil chilena.',
     'De "carro" o "carreta". Antiguamente se transportaban en carretas a las celebraciones campesinas. Con el tiempo, "carrete" derivo en la celebracion misma.',
     '["carretesito", "carretear"]'::jsonb),

    ('guata',
     'estomago, vientre, panza',
     'modismo',
     1, 1, 0,
     '/gwa.ta/',
     'Me duele la guata de tanto comer -> Me duele el estomago de tanto comer',
     'Uso cotidiano y no vulgar. Incluso usado en contextos medicos informales por pacientes.',
     'Del quechua "huata" (vientre, barriga). Una de las muchas palabras de origen indigena incorporadas al castellano chileno.',
     '[]'::jsonb),

    ('flaite',
     'persona de mal gusto, vulgar o de conducta antisocial',
     'insulto_ligero',
     1, 2, 3,
     '/flaj.te/',
     'Ese flaite se subio sin pagar el micro -> Ese delincuente se subio sin pagar el bus',
     'Termino clasista y despectivo. Originalmente asociado a estratos bajos, hoy se usa tambien para describir actitudes o gustos "ordinarios".',
     'Origen disputado: posiblemente del ingles "fly" (originalmente "elegante", luego ironico), del calo espanol "flaite", o de "flaites" (zapatillas marca Flait).',
     '["flaites"]'::jsonb),

    ('cuático',
     'extremo, alarmante, increible, fuera de lo normal',
     'modismo',
     2, 2, 1,
     '/kwa.ti.ko/',
     'Esta cuatica la situacion en la oficina -> Esta muy tensa la situacion en la oficina',
     'Se usa tanto para lo positivo como para lo negativo. "Cuatico" expresa que algo supera el umbral de lo normal.',
     'De "cuantico" (fisica cuantica), adoptado coloquialmente para describir algo "fuera de este mundo" o incomprensible.',
     '["cuatica"]'::jsonb),

    ('aperrar',
     'esforzarse, aguantar, persistir a pesar de las dificultades',
     'modismo',
     2, 1, 0,
     '/a.pe.rar/',
     'Vamos, aperra no mas que ya falta poco -> Vamos, aguanta que ya falta poco',
     'Expresion de aliento y resiliencia. Muy usada en contextos deportivos, laborales y de superacion personal.',
     'Metafora canina: asi como un perro (perro -> "perrar" -> "aperrar") se aferra a algo con tenacidad, la persona "aperra" para lograr su objetivo.',
     '[]'::jsonb),

    ('piola',
     'tranquilo, discreto, sigiloso, que no llama la atencion',
     'modismo',
     2, 0, 0,
     '/pjo.la/',
     'Mejor quedemonos piola en la reunion -> Mejor mantengamonos discretos en la reunion',
     'Tambien usado como advervio: "hacer algo piola" = hacerlo sin llamar la atencion.',
     'Del italiano "piola" (soga delgada) o del portugues "piola" (cuerda). La idea de algo delgado y silencioso derivo en "discreto".',
     '["piolita"]'::jsonb),

    ('brígido',
     'extremo, intenso, peligroso, fuera de control',
     'modismo',
     1, 2, 1,
     '/bɾi.xi.ðo/',
     'Estaba brigida la discusion en la reunion -> Estaba muy intensa la discusion en la reunion',
     'Originalmente "ebrio", pero hoy significa "intenso". Una de las pocas palabras chilenas que cambio de significado tan drasticamente.',
     'Posible deformacion de "ebrio" o influencia del ingles "british" (los soldados britanicos eran conocidos por su dureza). Origen incierto.',
     '["brigida"]'::jsonb),

    ('leseo',
     'tonto, persona que molesta o actua con poca seriedad',
     'insulto_ligero',
     1, 3, 2,
     '/le.se.o/',
     'No seai leso, esas son puras mentiras -> No seas ingenuo, esas son puras mentiras',
     'Puede ser insulto o expresion cariñosa segun el tono. "No sea leso" es una frase tipica chilena.',
     'Del español "leso" (tonto, necio). En Chile adquirio connotaciones menos severas que en otros paises.',
     '["lesera", "lesa"]'::jsonb),

    ('palta',
     'vergonzoso, problema, situacion incomoda',
     'jerga',
     2, 1, 0,
     '/pal.ta/',
     'Me dio una palta tener que pedirle plata -> Me dio verguenza tener que pedirle dinero',
     'No confundir con la fruta. "Dar palta" = dar verguenza. "Quedar palta" = quedar en ridiculo.',
     'Del quechua "palta" (carga, peso). La verguenza es una "carga" emocional. Sin relacion con el aguacate.',
     '["paltoso"]'::jsonb),

    ('tincada',
     'corazonada, presentimiento, intuicion',
     'modismo',
     2, 0, 0,
     '/tiŋ.ka.da/',
     'Me da la tincada que hoy va a llamar -> Tengo el presentimiento de que hoy va a llamar',
     'Se usa como "tincada" (sustantivo) o "tinca". Comun en conversaciones sobre predicciones informales.',
     'Del verbo "tincar". Origen mapuche o quechua. "Me tinca que..." es una de las frases chilenas mas reconocibles.',
     '["tinca"]'::jsonb),

    ('chori',
     'excelente, de buena calidad, impresionante',
     'modismo',
     1, 1, 0,
     '/tʃo.ɾi/',
     'La comida quedo chori -> La comida quedo excelente',
     'Abreviacion de "chorizo", pero con sentido positivo. No confundir con el embutido.',
     'Del español "chorizo" (ladron o ratero). En Chile la palabra dio un giro positivo: algo "roba-escena" o tan bueno que es "un robo".',
     '["chorizo", "chori"]'::jsonb),

    ('filete',
     'perfecto, excelente, en optimas condiciones',
     'modismo',
     2, 1, 0,
     '/fi.le.te/',
     'El auto esta filete -> El auto esta perfecto',
     'Expresion positiva pero menos intensa que "bacan". Denota que algo esta en buen estado o es correcto.',
     'Del italiano "filetto" (filete, corte fino de carne). Algo "filete" es de primera calidad.',
     '["fileteque"]'::jsonb);

-- 3. Frases -----------------------------------------------------------------
INSERT INTO frase (escenario_id, frase_original, traduccion, explicacion, tono, intencion_real, nivel_formalidad, nivel_ironia, nivel_sarcasmo, ejemplo_uso) VALUES
    -- Amigos (3)
    (3,
     '¿Cachai lo que te digo?',
     '¿Entiendes lo que te digo?',
     'Muletilla para confirmar comprension. Similar al "you know what I mean?" del ingles. Se usa constantemente para verificar que el interlocutor sigue la conversacion.',
     'neutro',
     'Verificar que el interlocutor esta comprendiendo y sigue activamente la conversacion.',
     1, 1, 0,
     'Despues de explicar algo complicado: "Entonces el weon se fue con la plata, cachai lo que te digo?"'),
    (3,
     'Estaba brigida la wea',
     'La situacion estaba muy intensa o peligrosa',
     'Frase comodin para describir cualquier situacion extrema. "Brigido" = intenso, "wea" = cosa/situacion. Juntos enfatizan lo fuera de lo comun de una experiencia.',
     'directo',
     'Expresar que una experiencia fue emocional o fisicamente intensa, generando complicidad con el oyente.',
     1, 2, 1,
     'Llegando a la casa: "Nos fuimos en la micro y habia un flaite gritando... estaba brigida la wea."'),
    (3,
     'Me tinca que va a llegar tarde',
     'Tengo el presentimiento de que va a llegar tarde',
     'Expresar una opinion basada en intuicion. "Tincar" es tener un presentimiento. Es una forma suave de hacer una prediccion sin tener evidencia concreta.',
     'neutro',
     'Compartir una opinion o intuicion sin sonar arrogante ni afirmativo.',
     2, 0, 0,
     'Mirando el reloj: "Son las 9 y el entra a las 8:30... me tinca que va a llegar tarde."'),

    -- Fiesta / Carrete (6)
    (6,
     'Bacan el carrete de anoche',
     'Excelente la fiesta de anoche',
     'Expresion tipica para evaluar positivamente un evento social. "Bacan" = genial, "carrete" = fiesta. Denota que la experiencia fue muy satisfactoria.',
     'directo',
     'Expresar satisfaccion y entusiasmo por un evento social reciente.',
     2, 0, 0,
     'Llamando a un amigo al dia siguiente: "Oye, bacan el carrete de anoche, deberiamos repetir."'),
    (6,
     'Vamos a carretear este finde',
     'Vamos a ir de fiesta este fin de semana',
     '"Carretear" es el verbo para salir de fiesta o celebrar. Implica salir a bailar, beber y socializar activamente.',
     'directo',
     'Proponer un plan social de forma entusiasta.',
     1, 0, 0,
     'En el trabajo el viernes: "Ya po, vamos a carretear este finde, nos merecemos un descanso."'),

    -- Trabajo (4)
    (4,
     'Estoy chato de esta pega',
     'Estoy harto de este trabajo',
     'Expresion de agotamiento laboral. "Chato" = aplanado metaforicamente. "Pega" = trabajo. Comun en conversaciones de camaraderia laboral.',
     'directo',
     'Desahogar frustracion laboral con un colega de confianza.',
     1, 1, 0,
     'En la cafeteria con un companero: "Llevo tres meses haciendo lo mismo, estoy chato de esta pega."'),
    (4,
     'Aperrando no mas',
     'Aguantando y perseverando a pesar de todo',
     'Frase de resiliencia tipica chilena. Indica que la persona sigue adelante pese a las dificultades, con una actitud de resistencia estoica.',
     'motivacional',
     'Manifestar determinacion y compromiso para continuar a pesar de las adversidades.',
     2, 0, 0,
     'El jefe pregunta como va el proyecto: "Ahi vamos, aperrando no mas, pero vamos a cumplir."'),
    (4,
     'El jefe esta puro webiando con el proyecto',
     'El jefe esta perdiendo el tiempo o no tomando en serio el proyecto',
     '"Webiar/webiar" es actuar sin seriedad, distraerse o procrastinar. Deriva de "weon". Expresa frustracion por falta de seriedad de un superior.',
     'ironico',
     'Expresar frustracion ante la percepcion de que un lider no esta tomando el trabajo con la seriedad debida.',
     1, 3, 2,
     'En el almuerzo con colegas: "Llevamos un mes esperando su decision, el jefe esta puro webiando."'),

    -- Familia (5)
    (5,
     'No seai leso, abrigate',
     'No seas tonto, abrigate',
     'Frase de preocupacion familiar con tono cariñoso. "Leso" aqui no es insulto sino expresion de cuidado. Tipico de madres y abuelas chilenas.',
     'directo',
     'Expresar preocupacion por el bienestar de un ser querido usando un tono fraternal y cercano.',
     2, 0, 0,
     'Al salir de la casa: "Hijo, no seai leso, abrigate que hace frio."'),
    (5,
     'Puro webiando todo el dia',
     'Pasaste todo el dia sin hacer nada productivo',
     'Reproche informal tipico. "Webiar" es perder el tiempo. Se usa entre familiares para senalar falta de productividad con un tono que mezcla reproche y cariño.',
     'ironico',
     'Senalar de manera informal que alguien no ha sido productivo durante el dia.',
     1, 3, 1,
     'La mama al hijo que llega del trabajo: "¿Y? ¿Puro webiando todo el dia en la calle?"'),

    -- Entrevista laboral (1)
    (1,
     'Estoy dando jugo',
     'Estoy poniendome nervioso o actuando de forma forzada',
     '"Dar jugo" es ponerse excesivamente nervioso en una situacion formal, actuando de manera tensa o poco natural. Similar a "overthinking" en ingles.',
     'neutro',
     'Reconocer el propio nerviosismo o ansiedad en una situacion de presion.',
     2, 1, 0,
     'Antes de entrar a la entrevista: "Estoy dando jugo con esto, voy a respirar profundo."'),
    (1,
     'Echar la talla en la entrevista',
     'Hacer bromas o comentarios graciosos en la entrevista',
     '"Echar la talla" es bromear o hacer chistes. En contexto de entrevista, se refiere a intentar aliviar la tension con humor, lo cual puede ser arriesgado.',
     'humoristico',
     'Describir un intento de usar el humor para manejar una situacion formal y tensa.',
     2, 2, 0,
     'Practicando la entrevista: "Le eche la talla con el tema del trafico y el entrevistador se rio."'),

    -- Medico (2)
    (2,
     'Me duele la guata',
     'Me duele el estomago / abdomen',
     'Forma coloquial pero no vulgar de describir dolor abdominal. Los propios medicos chilenos entienden y usan "guata" con pacientes.',
     'directo',
     'Describir un sintoma fisico de manera coloquial y comprensible.',
     2, 0, 0,
     'En la consulta: "Doctor, desde ayer me duele la guata y no he podido comer bien."'),
    (2,
     'Estoy cuatico con los examenes',
     'Estoy muy preocupado o ansioso por los examenes medicos',
     '"Cuatico" expresa que algo te afecta profundamente. En este contexto, denota ansiedad significativa por resultados medicos.',
     'directo',
     'Expresar ansiedad o preocupacion intensa por resultados de examenes de salud.',
     2, 0, 0,
     'Esperando resultados: "Estoy cuatico con los examenes, no he podido dormir bien."');

-- 4. Frase-Palabra (relaciones N:M) -----------------------------------------
INSERT INTO frase_palabra (frase_id, palabra_id, relevancia) VALUES
    -- "Cachai lo que te digo?" -> cachai
    (1, 4, 5),
    -- "Estaba brigida la wea" -> brigido, weon
    (2, 15, 5),
    (2, 1, 4),
    -- "Me tinca que va a llegar tarde" -> tincada
    (3, 18, 5),
    -- "Bacan el carrete de anoche" -> bacan, carrete
    (4, 3, 5),
    (4, 9, 5),
    -- "Vamos a carretear este finde" -> carrete
    (5, 9, 4),
    -- "Estoy chato de esta pega" -> chato, pega
    (6, 6, 5),
    (6, 7, 5),
    -- "Aperrando no mas" -> aperrar
    (7, 13, 5),
    -- "El jefe esta puro webiando" -> weon
    (8, 1, 3),
    -- "No seai leso" -> leseo
    (9, 16, 5),
    -- "Puro webiando" -> weon
    (10, 1, 4),
    -- "Dar jugo" (frase sin palabra directa asociada)
    -- "Echar la talla" (frase sin palabra directa asociada)
    -- "Me duele la guata" -> guata
    (13, 10, 5),
    -- "Estoy cuatico" -> cuatico
    (14, 12, 5);

-- 5. Usuario de prueba ------------------------------------------------------
INSERT INTO usuario (nombre, email, contrasena_hash, preferencias, activo)
VALUES (
    'Usuario Prueba',
    'test@desenreda.cl',
    '$2b$12$LJ3m4ys3Lk0TSwHnbfOMiOXPm1Qlq5Gz5Y5p5Y5p5Y5p5Y5p5Y5',
    '{"tono_explicacion": "neutro", "nivel_detalle": "medio"}'::jsonb,
    TRUE
);

-- 6. Sugerencias de ejemplo -------------------------------------------------
INSERT INTO sugerencia (usuario_id, tipo, contenido, estado, usuario_email) VALUES
    -- Sugerencia de palabra anonima
    (NULL,
     'palabra',
     '{"palabra": "cahuin", "traduccion": "chisme, conflicto o intriga", "categoria": "modismo", "ejemplo_uso": "Se armo el cahuin en la oficina cuando supieron lo del ascenso", "nota_cultural": "Del mapudungun ''cahuin'' (reunion o junta). Originalmente una reunion social, derivo a reunion donde se chismea."}',
     'pendiente',
     'anonimo@correo.cl'),

    -- Sugerencia de frase de usuario registrado
    (1,
     'frase',
     '{"frase_original": "Estoy chato de todo", "traduccion": "Estoy cansado de la situacion general", "escenario_id": 4, "explicacion": "Expresion de hartazgo generalizado, no dirigido a algo especifico sino a la situacion completa.", "tono": "directo", "nivel_formalidad": 1}',
     'pendiente',
     NULL),

    -- Sugerencia de escenario anonima
    (NULL,
     'escenario',
     '{"nombre": "Supermercado", "descripcion": "Situaciones cotidianas en el supermercado donde ocurren interacciones con personal y otros clientes", "icono": "cart"}',
     'aprobado',
     'colaborador@correo.cl');

-- 7. Verificacion de datos insertados ---------------------------------------
-- Descomentar para verificar:
-- SELECT 'Escenarios' AS tabla, COUNT(*) FROM escenario
-- UNION ALL SELECT 'Palabras', COUNT(*) FROM palabra
-- UNION ALL SELECT 'Frases', COUNT(*) FROM frase
-- UNION ALL SELECT 'Frase-Palabra', COUNT(*) FROM frase_palabra
-- UNION ALL SELECT 'Usuarios', COUNT(*) FROM usuario
-- UNION ALL SELECT 'Sugerencias', COUNT(*) FROM sugerencia;
