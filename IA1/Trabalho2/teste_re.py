import spacy
import PyPDF2
import re
import unicodedata

def concatenate_word():
    global texto
    text_lines = texto.splitlines()

    for i in range(len(text_lines)):
        if len(text_lines[i]) == 0:
            continue

        if (text_lines[i][-1] == "-"):
            next_line_words = text_lines[i+1].split(" ")
            text_lines[i] = text_lines[i][:-1] + next_line_words[0] + " "
            text_lines[i+1] = ' '.join(next_line_words[1:])
        text_lines[i] = text_lines[i] + " "
    texto = ''
    for i in text_lines:
        texto += i

def normalizacao():
    global texto
    # td em minusculo
    texto = texto.lower()

    # acentos e especiais
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')

    # substitui abreviações p inteiras
    texto = texto.replace('fig.', 'figure')
    texto = texto.replace('e.g.', 'for example')
    texto = texto.replace('et al.', 'and others')
    texto = texto.replace('ch.', 'chapter')
    texto = texto.replace('sec.', 'section')
    texto = texto.replace('ref.', 'reference')
    texto = texto.replace('app.', 'appendix')


# realiza a limpeza dos texto
def preprocessamento():
    global texto

    concatenate_word()
    
    # Remove quebra de linha
    texto = re.sub(r'\n', ' ', texto)
    # texto = re.sub(r'\.', ' ', texto)

    ## essas pontuacao e numeros é importante p filtrar as secao se pa
    # texto = re.sub(r'[^a-zA-Z\s]', '', texto)
    # print(texto)
    normalizacao()

    # lematizacao seria importante? => palavras na forma basica
    
    # Remove referencia
    references_regex = re.compile(r"References.*", re.IGNORECASE)
    texto = references_regex.sub("References", texto)



# python -m spacy download pt_core_news_sm
# carrega o modelo do spacy em ingles
# python -m spacy download en_core_web_sm
nlp = spacy.load('en_core_web_sm')

# define o texto do artigo
# texto = "O objetivo deste artigo é apresentar uma revisão bibliográfica sobre o uso de inteligência artificial na área da saúde."

# texto = "analysis of the impact of cyber attack on semiconductor manufacturing energy quantification busra ezici paulo costa jie xu systems engineering and operations research george mason university 4400 university dr fairfax, v a, usa {bozoglu, pcosta, jxu13}@gmu.edu annsim22, july 18-20, 2022, san diego, ca, usa; 2022 society for modeling & simulation international (scs)abstract semiconductor manufacturers deal with complex processes, diverse product lines, and rapidly changing technologies while facing a competitive global market. there is also increased adoption of digital technologies  with globalization, which creates an interconnection between each process. digital connectivity and adaptation to advanced automated technologies increase dependence on data and the vulnerability to cyber-attacks. the presence of cyber-attacks in manufacturing causes delays in processing times for manufacturing,  which impact performance and energy consumption. this study proposes a framework consisting of an energy quantication model, cyber risk modeling, and simulation analyses to address the impact of cyber threats on the energy quantication of semiconductor manufacturing. the performance of the wafer fab is analyzed using the cycle time, throughput rate, and work-in-process level since they lead to the energy quantication in processes. then the cyber-attack scenario is included in the simulation model to evaluate the impact of the cyberattack on energy quantication. keywords:semiconductor manufacturing, simulation analysis, workow modeling, cyber-attacks 1 introduction a semiconductor, also known as integrated circuits (ics), or chips, is a tiny electronic device composed of many components that store, move, and process data (platzer, jr, and sutter 2020). the manufacturing of semiconductors begins with the arrival of raw input and materials, which is then followed by front-end (wafer fab) and back-end operations (assembly, sort, test) (kannaian 2018). in a wafer fab,rst, a furnace forms a cylinder of silicon or other semiconducting materials, which is then cut into disc-shaped wafers. a chip may contain so many layers in total and require many chemical processes such as deposition, oxidation,  diffusion, photolithography, etching, photoresisting, layering, and doping. deposition tools form the basis of a new permanent layer by adding a materiallm. then, the photolithography process draws circuit patterns in the layer, starting with coating a photoresist on the deposited material. a photolithography tool passes light through a photomask to transfer that pattern to the photoresist. the light dissolves parts of the photoresist considering the circuit pattern. etching is the tool carving the newly created pattern in the photoresist  into the permanent layer below the photoresist. the photoresist is removed, and the etched material is cleaned off the layer. other times, atoms are embedded into the layer in an ion implantation process 258 authorized licensed use limited to: universidade estadual de maringa. downloaded on april 16,2023 at 02:30:55 utc from ieee xplore.  restrictions apply. ezici, costa, and xu instead of etching. then, the completed layer isattened with chemical mechanical planarization(cmp) process. this allows a new layer to be added, and the cycle begins again. process control tools are used to inspect the wafer and its layers throughout fabrication to ensure no errors in the system (khan 2021). this process requires 300 to 700 different processing steps and makes it the most complex portion of the entire manufacturing process (kannaian 2018). assembly, testing, and packaging (atp) are also known as back-end processes. the wafer is cut into individual ics, also known as dies, and the failed ics are scrapped (kannaian 2018). the assembly phase starts with cutting anished wafer into separate chips. each chip is attached to a frame with wires that connect the chip to external devices and enclosed in a protective casing, so a dark gray rectangle with metal pins at the edges produces anal look. the testing procedure is also applied to the chips to ensure it operates as intended (khan 2021). the us depends on global supply chains and production concentrated in east asia. therefore, vulnerability to disruption or denial due to trade disputes could be detrimental. manufacturing disruptions during the covid-19 pandemic have signicantly increased this concern. so, it is very important to improve processes and expand/retain advanced domestic semiconductor fabrication plants (platzer, jr, and sutter 2020). also, high-tech fabrication plants used for the production of the semiconductor or thin-lm-transistor liquid crystal display (tft-lcd) are energy and technology-intensive industries (hu, lin, fu, chang, and cheng 2019). in addition to a very competitive global market and energy intensity, semiconductor manufacturers must deal with complex processes, sophisticated equipment, diverse product lines, and rapidly changing technologies. the digitization in the industry increases dependence on data, and the adaptation with advanced automated technologies increases the vulnerability for cyber-attacks (laboratory 2020). the presence of cyber attack in manufacturing cause delays in processing times for manufacturing (avila 2017) and have an impact on production performance and energy consumption. the objective of this study is to establish and assess performance metrics by exploring the modeling and simulation of semiconductor wafer fab manufacturing processes, with the goal of providing an energy quantication  framework for semiconductor manufacturing in the presence of a cyber attack. this study also aims to provide a cyber risk assessment framework for semiconductor manufacturing. this analysis included  three important steps: the energy quantication model, cyber risk analysis framework, and simulation  analysis. the rest of the paper is organized as follows. section 2 provides the related literature. section 3 introduces the methodology for energy quantication, cyber risk quantication framework, and simulation model. section 4 proposed the experimental analysis for intel minifab model. the research is concluded, and further research directions are provided in section 5. 2 literature review several studies in literature are relevant to our research, which include simulation modeling of semiconductor  manufacturing, general cyber threats in manufacturing, and cyber risk assessment with simulations. (rose 2000) analyzed the behavior of complex wafer fabs in certain scenarios by estimating cycle time and wip level using simulation on the mimac dataset. (morrice, valdez, chida, and eido 2005) proposed a model for supply chain planning and inventory control to predict the effect of internal on-time delivery, inventory, and wip changes on the customer order fulllment service level by using simulation. their work was based on historical data and expert opinion. (li, ramirez-hernandez, fernandez, mclean, and leong 2005) proposed a model for standard modular simulation of semiconductor wafer fabrication facilities.  they used the intel minifab model to analyze the impact of the workforce in production performance using cycle time, throughput rate, and wip level as performance metrics. (liu, li, yang, wan, and uzsoy 2011) proposed production planning for semiconductor manufacturing via simulation optimization. (valente,  christiano cecone, alvim, and cassiano 2015) aimed to optimize the semiconductor manufacturing process using variation in the number of machines and operators. they used the intel five-machine six-step mini-fab model during experimental analysis but considered only two different entities as input and ignored 259 authorized licensed use limited to: universidade estadual de maringa. downloaded on april 16,2023 at 02:30:55 utc from ieee xplore.  restrictions apply. ezici, costa, and xu the test wafer. also, preventive maintenance time was different for each cell from the real case study for intel  minifab (ie 4803 intel mini fab case study - model-based systems engineering and the intel minifab case leon, n.d.). they assumed that allve machines presented in the model require 30-minute preventive  maintenance every 12 hours. they also ignored the stocker requirement (buffer capacity) in each cell during the modeling. (shinde 2018) proposed modeling and simulation of a semiconductor manufacturing fab for cycle time analysis. the thesis analyzes the effects of scheduling policies and machine failures on the manufacturing cycle time of the ic manufacturing process for two processor chips, namely skylake and kabylake, manufactured by intel. (werling, yugma, soukhal, and mohr 2020) proposed an agent-based simulation model with human resource integration for semiconductor manufacturing facility. all these studies  focus on cycle time, wip, and throughput rate. in comparison, this study uses a framework for energy quantication. similar work is (kannaian 2018), which proposed two methods to estimate electric energy consumption and carbon dioxide emission of a semiconductor wafer fab. they analyzed the impact of wafer starts per year and product mix, but they did not consider the cyber threat impact on manufacturing. (bracho,  saygin, wan, lee, and zarreh 2018) introduces a simulation model to assess the repercussions on manufacturing systems performance in the presence of cyber threats, but they did not include the impact on energy quantication. this study contributes to the literature by integrating cyber-attack into semiconductor manufacturing simulation modeling to analyze the impact of cyber-attack on energy quantication. the cybersecurity threats and vulnerabilities of the general manufacturing processes are analyzed through the literature. those are mostly derived from emerging technologies. (sobb, turnbull, and moustafa 2020) investigated the threats against 5g and wireless communication, cloud computing, iot"
path = './papers/Internet_of_Things_Platform.pdf'
# path = './papers/ANALYSIS_OF_THE_IMPACT.pdf'
# path = './papers/Attributes_and_Entrepreneurial.pdf'

# path = './image_processing/Going_deeper_with_convolutions.pdf'
# path = './image_processing/Histograms_of_oriented_gradients_for_human_detection.pdf'
# path = './image_processing/Image_quality_assessment_from_error_visibility_to_structural_similarity.pdf'
# path = './image_processing/You_Only_Look_Once_Unified_Real-Time_Object_Detection.pdf'

# path = './artificial_intelligence/Densely_Connected_Convolutional_Networks.pdf'

# Le todas a paginas do pdf
with open(path, 'rb') as pdf_file:
    # Cria obj de leitura do pdf
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    info = pdf_reader.metadata
    texto = ''
    # for i in range(len(pdf_reader.pages)):
    for i in range(len(pdf_reader.pages)):
        pdf_page = pdf_reader.pages[i]
        texto += pdf_page.extract_text()
        # print(texto)

# concatenate_word()
# texto = re.sub(r'\n', ' ', texto)
# rever no preprocessamento
texto = texto.replace('Methodology. ', 'Methodology ') 
texto = texto.replace('Methodology: ', 'Methodology ') 
texto = texto.replace('Objective. ', 'Objective ') 
texto = texto.replace('Objective: ', 'Objective ') 
# texto = texto.replace(':', '-') 
# texto = re.sub(r':', ';', texto) 
preprocessamento()

# processa o texto com o spacy
doc = nlp(texto)

obj_bool = False
problem_bool = False
method_bool = False
contrib_bool = False
defPinta = False
# percorre as sentenças do texto
print(texto)
for sent in doc.sents:
    # verifica se a sentença contém as palavras "objective" e "research"
    if not obj_bool and "objective" in sent.text.lower() and ("study" in sent.text.lower() or "research" in sent.text.lower() or "article" in sent.text.lower() or "main" in sent.text.lower()):
        print
        # extrai a parte do texto que segue a palavra "objetivo"
        objetivo = sent.text.split("objective")[1].strip()
        # imprime o objetivo na tela
        print("\nO objetivo do artigo é:", objetivo)
        obj_bool = True

    if not obj_bool and ("purpose" in sent.text.lower() or "purposes" in sent.text.lower()) and ("study" in sent.text.lower() or "research" in sent.text.lower() or "article" in sent.text.lower() or "main" in sent.text.lower()):
        # extrai a parte do texto que segue a palavra "purpose"
        objetivo = sent.text.split("purpose")[1].strip()
        # imprime o objetivo na tela
        print("\nO objetivo do artigo é:", objetivo)
        obj_bool = True

    # verifica se a sentença contém as palavras "problem"
    if not problem_bool and "problem" in sent.text.lower() and ("study" in sent.text.lower() or "research" in sent.text.lower()) and not "objective" in sent.text.lower():
        # extrai a parte do texto que segue a palavra "problem"
        problem = sent.text.split("problem")[1].strip()
        # imprime o problem na tela
        print("\nO problema citado no artigo é:", problem)
        problem_bool = True

    if not problem_bool and "issue" in sent.text.lower() and ("study" in sent.text.lower() or "research" in sent.text.lower()) and not "objective" in sent.text.lower():
        # extrai a parte do texto que segue a palavra "problem"
        problem = sent.text.split("issue")[1].strip()
        # imprime o problem na tela
        print("\nProblema/Issue:", problem)
        problem_bool = True

    # verifica se a sentença contém as palavras "methodology"
    if not method_bool and "methodology" in sent.text.lower() and ("study" in sent.text.lower() or "research" in sent.text.lower() or "examples" in sent.text.lower() or "model" in sent.text.lower() or "use" in sent.text.lower() or "papers" in sent.text.lower()):
        # extrai a parte do texto que segue a palavra "methodology"
        try:
            methodology = sent.text.split("methodology")[1].strip()
        except:
            methodology = sent.text.split("methodology")[0].strip()

        # imprime o methodology na tela
        print("\nMetodologia:", methodology)
        method_bool = True

    # verifica se a sentença contém as palavras "contributes"
    if not contrib_bool and "contributes" in sent.text.lower():
        # extrai a parte do texto que segue a palavra "contributes"
        contributes = sent.text.split("contributes")[1].strip()
        # imprime o contributes na tela
        print("\nContribuição:", contributes)
        contrib_bool = True
