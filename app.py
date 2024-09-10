from flask import Flask, render_template, request, send_file
import os
from pdfrw import PdfReader, PdfWriter, PageMerge
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gerar-documento', methods=['POST'])
def gerar_documento():
    # Capturar os dados do formulário
    nome_completo = request.form['nomecompleto']
    rg = request.form['rg']
    cpf = request.form['cpf']
    unidade = request.form['unidade']
    modulo = request.form['modulo']
    responsavel = request.form['responsavel']
    carga = request.form['carga']
    data = request.form['data']
    resumo = request.form['resumo']
    sintome = request.form['sintome']
    tipo_pessoa = request.form['tipo_pessoa']

    # Caminho para o PDF modelo
    caminho_pdf = os.path.join('documentos', 'TERMO_DE_VALIDAÇÃO_E_PRESENÇA_NO_MÓDULO_DE_TREINAMENTO2.pdf')

    # Ler o PDF
    pdf_reader = PdfReader(caminho_pdf)
    pdf_writer = PdfWriter()

    # Mapeamento dos campos de formulário e dados
    data_mapping = {
        'NOMECOMPLETO': nome_completo,
        'RG': rg,
        'CPF': cpf,
        'UNIDADE/TERRITORIO': unidade,
        'MODULO': modulo,
        'RESPONSAVEL': responsavel,
        'CARGA': carga,
        'DATA': data,
        'RESUMO': resumo,
        'SINTOME': sintome,
        'FRANQUEADO/SOCIO/FAMILIAR': tipo_pessoa
    }

    # Preencher os campos de formulário no PDF
    for page in pdf_reader.pages:
        annotations = page['/Annots']
        if annotations:
            for annotation in annotations:
                field = annotation.getObject()
                field_name = field.get('/T')  # Nome do campo
                if field_name in data_mapping:
                    field.update({
                        '/V': data_mapping[field_name],  # Substitui o valor do campo
                        '/Ff': 1  # Define o campo como preenchido
                    })
        pdf_writer.addpage(page)

    # Escrever o novo PDF em um buffer
    output_pdf = BytesIO()
    pdf_writer.write(output_pdf)
    output_pdf.seek(0)

    # Enviar o PDF preenchido para o navegador
    return send_file(output_pdf, as_attachment=False, download_name='termo_preenchido.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
