import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
from partidos import obter_filtro_usuario, funcao_normalizacao

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualização de Dados Políticos")
        self.root.geometry("800x600")
        #self.root.configure(bg="#E6F0F5")

        self.header_frame = tk.Frame(root, bg= "#005A8C")
        self.header_frame.pack(fill="both")


        self.title_image_frame = tk.Frame(self.header_frame, bg="#005A8C")
        self.title_image_frame.pack()

        self.subheading_frame = tk.Frame(self.header_frame, bg = "#090245")
        self.subheading_frame.pack(fill = "both")

        # Título
        self.title_label = tk.Label(self.title_image_frame, text="RELAÇÃO PARTIDOS E DEPUTADOS", bg="#005A8C", fg="white", font=("Helvetica", 18, "bold"))
        self.title_label.grid(row = 0, column = 1, padx = 2.5, pady = 5)

        # Carregando a imagem
        self.imagem = Image.open("bandeira.png")
        self.imagem.thumbnail((50, 50))
        self.imagem = ImageTk.PhotoImage(self.imagem)

        self.imagem_label = tk.Label(self.title_image_frame, image=self.imagem, bg="#005A8C")
        self.imagem_label.grid(row = 0, column = 0, padx = 2.5, pady = 5)

        self.subheader_label = tk.Label(self.subheading_frame, text = "Obtenha o Grafo, HeatMap e Betweenness desejado!", font = ("verdana", "10"),bg = "#090245", fg = "#dad6ff")
        self.subheader_label.pack(pady = 5)

        self.frame = tk.Frame(root)
        self.frame.pack(pady=20) 

        self.label_ano = tk.Label(root, text="Digite o ano:", font = ("Helvetica", 10))
        self.label_ano.pack()

        self.ano_entry = tk.Entry(root)
        self.ano_entry.pack()

        self.label_partidos = tk.Label(root, text="Digite os partidos (separados por vírgula) ou 'todos' para todos os partidos:", font = ("Helvetica", 10))
        self.label_partidos.pack()

        self.partidos_entry = tk.Entry(root)
        self.partidos_entry.pack()

        self.label_threshold = tk.Label(root, text="Digite o threshold:", font = ("Helvetica", 10))
        self.label_threshold.pack()

        self.threshold_entry = tk.Entry(root)
        self.threshold_entry.pack()

        self.generate_button = tk.Button(root, text="Gerar Visualização", command=self.generate_visualization, bg="#005A8C", fg="white", font=("Helvetica", 10, "bold"))
        self.generate_button.pack(pady=15)
        
        
        self.image_frame = tk.Frame(root)
        self.image_frame.pack()

        self.image_label_plotagem = tk.Label(self.image_frame)
        self.image_label_plotagem.pack(side=tk.LEFT, padx=10)  # Espaço horizontal entre as labels

        self.image_label_representacao = tk.Label(self.image_frame)
        self.image_label_representacao.pack(side=tk.LEFT, padx=10)

        self.image_label_heatmap = tk.Label(self.image_frame)
        self.image_label_heatmap.pack(side=tk.LEFT)

        self.empty_label = tk.Label(root)
        self.empty_label.pack()

        self.scroll_canvas = tk.Canvas(root)
        self.scroll_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scroll_y = tk.Scrollbar(root, orient=tk.VERTICAL, command=self.scroll_canvas.yview, )
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.scroll_canvas.configure(yscrollcommand=self.scroll_y.set)

        self.scroll_x = tk.Scrollbar(root, orient=tk.HORIZONTAL, command=self.scroll_canvas.xview)
        self.scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.scroll_canvas.configure(xscrollcommand=self.scroll_x.set)

        self.canvas_frame = tk.Frame(self.scroll_canvas)
        self.scroll_canvas.create_window((0, 0), window=self.canvas_frame, anchor="nw")

        # Adicionar frames para as imagens
        self.frame_plotagem = tk.Frame(self.canvas_frame)
        self.frame_plotagem.pack(padx=10, pady=10, side=tk.LEFT)

        self.frame_representacao = tk.Frame(self.canvas_frame)
        self.frame_representacao.pack(padx=10, pady=10, side=tk.LEFT)

        self.frame_heatmap = tk.Frame(self.canvas_frame)
        self.frame_heatmap.pack(padx=10, pady=10, side=tk.LEFT)

        # Atualizar a configuração da canvas quando o tamanho do frame interno mudar
        self.canvas_frame.bind("<Configure>", self.on_frame_configure)

    def on_frame_configure(self, event):
        # Atualizar a região de rolagem quando o tamanho do frame interno mudar
        self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))

    def add_image_to_frame(self, frame, image_path):
        img = Image.open(image_path)
        img.thumbnail((800, 800))
        img = ImageTk.PhotoImage(img)

        label = tk.Label(frame, image=img)
        label.image = img
        label.pack()

    def generate_visualization(self):
        ano = self.ano_entry.get()
        partidos_input = self.partidos_entry.get()

        if partidos_input.lower() == 'todos':
            partidos = []  # Lista vazia indica todos os partidos
        else:
            partidos = partidos_input.split(',')

        threshold = self.threshold_entry.get()

        funcao_normalizacao(partidos, ano, threshold)

        self.add_image_to_frame(self.frame_plotagem, "representacao_plotagem.png")
        self.add_image_to_frame(self.frame_representacao, "representacao_grafico.png")
        self.add_image_to_frame(self.frame_heatmap, "representacao_heatmap.png")

if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()
