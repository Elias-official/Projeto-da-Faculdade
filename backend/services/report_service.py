import csv
import io
from datetime import datetime, timedelta


def dashboard_resumo(conn):
    """Gera resumo do dashboard com métricas principais."""
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) AS total_produtos FROM produtos')
    total_produtos = cursor.fetchone()['total_produtos'] or 0

    cursor.execute('SELECT SUM(estoque_atual) AS estoque_total FROM produtos')
    estoque_total = cursor.fetchone()['estoque_total'] or 0

    cursor.execute('SELECT COUNT(*) AS estoque_baixo FROM produtos WHERE estoque_atual <= estoque_minimo')
    estoque_baixo = cursor.fetchone()['estoque_baixo'] or 0

    cursor.execute('SELECT SUM(estoque_atual * preco) AS valor_estoque FROM produtos')
    valor_estoque = cursor.fetchone()['valor_estoque'] or 0

    # Movimentações de hoje
    hoje = datetime.now().date()
    cursor.execute('SELECT COUNT(*) AS movimentacoes_hoje FROM movimentacoes WHERE DATE(data_movimentacao) = ?', (hoje,))
    movimentacoes_hoje = cursor.fetchone()['movimentacoes_hoje'] or 0

    # Produtos críticos
    cursor.execute('SELECT COUNT(*) AS criticos FROM produtos WHERE estoque_atual <= 5')
    produtos_criticos = cursor.fetchone()['criticos'] or 0

    return {
        'total_produtos': total_produtos,
        'estoque_total': estoque_total,
        'estoque_baixo': estoque_baixo,
        'valor_estoque': round(valor_estoque or 0, 2),
        'movimentacoes_hoje': movimentacoes_hoje,
        'produtos_criticos': produtos_criticos
    }


def categorias_por_produto(conn):
    """Retorna distribuição de produtos por categoria."""
    cursor = conn.cursor()
    cursor.execute('SELECT categoria, COUNT(*) AS total FROM produtos GROUP BY categoria ORDER BY total DESC')
    return [dict(row) for row in cursor.fetchall()]


def movimentacoes_por_tipo(conn):
    """Retorna total de movimentações agrupadas por tipo."""
    cursor = conn.cursor()
    cursor.execute('SELECT tipo, SUM(quantidade) AS total FROM movimentacoes GROUP BY tipo')
    return [dict(row) for row in cursor.fetchall()]


def relatorio_periodo(conn, data_inicio, data_fim):
    """Gera relatório de movimentações em um período."""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT 
            m.id,
            p.produto,
            u.nome AS usuario,
            m.tipo,
            m.quantidade,
            m.data_movimentacao,
            p.preco
        FROM movimentacoes m
        LEFT JOIN produtos p ON p.id = m.produto_id
        LEFT JOIN usuarios u ON u.id = m.usuario_id
        WHERE DATE(m.data_movimentacao) BETWEEN ? AND ?
        ORDER BY m.data_movimentacao DESC
    ''', (data_inicio, data_fim))
    rows = cursor.fetchall()
    return [dict(row) for row in rows]


def produtos_mais_movimentados(conn, limite=10):
    """Retorna produtos mais movimentados."""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT 
            p.id,
            p.produto,
            COUNT(m.id) AS total_movimentacoes,
            SUM(m.quantidade) AS quantidade_total
        FROM produtos p
        LEFT JOIN movimentacoes m ON m.produto_id = p.id
        GROUP BY p.id, p.produto
        ORDER BY total_movimentacoes DESC
        LIMIT ?
    ''', (limite,))
    return [dict(row) for row in cursor.fetchall()]


def estatisticas_estoque(conn):
    """Retorna estatísticas completas de estoque."""
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) AS total FROM produtos WHERE estoque_atual = 0')
    zerados = cursor.fetchone()['total'] or 0
    
    cursor.execute('SELECT COUNT(*) AS total FROM produtos WHERE estoque_atual <= 5')
    criticos = cursor.fetchone()['total'] or 0
    
    cursor.execute('SELECT COUNT(*) AS total FROM produtos WHERE estoque_atual > 5 AND estoque_atual <= estoque_minimo')
    baixos = cursor.fetchone()['total'] or 0
    
    cursor.execute('SELECT COUNT(*) AS total FROM produtos WHERE estoque_atual > estoque_minimo')
    normais = cursor.fetchone()['total'] or 0
    
    return {
        'zerados': zerados,
        'criticos': criticos,
        'baixos': baixos,
        'normais': normais
    }


def valor_total_estoque_por_categoria(conn):
    """Retorna valor total do estoque por categoria."""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT 
            categoria,
            COUNT(*) AS total_produtos,
            SUM(estoque_atual) AS estoque_total,
            SUM(estoque_atual * preco) AS valor_total
        FROM produtos
        GROUP BY categoria
        ORDER BY valor_total DESC
    ''')
    return [dict(row) for row in cursor.fetchall()]


def export_produtos_csv(conn):
    """Exporta produtos em CSV."""
    cursor = conn.cursor()
    cursor.execute('SELECT codigo, produto, marca, categoria, estoque_atual, estoque_minimo, preco, status, criado_em FROM produtos ORDER BY produto')
    rows = cursor.fetchall()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Código', 'Produto', 'Marca', 'Categoria', 'Estoque Atual', 'Estoque Mínimo', 'Preço', 'Status', 'Criado em'])
    for row in rows:
        writer.writerow([
            row['codigo'],
            row['produto'],
            row['marca'],
            row['categoria'],
            row['estoque_atual'],
            row['estoque_minimo'],
            f"R$ {row['preco']:.2f}",
            row['status'],
            row['criado_em']
        ])
    return output.getvalue()


def export_movimentacoes_csv(conn):
    """Exporta movimentações em CSV."""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT m.id, p.produto AS produto, u.username AS usuario, m.tipo, m.quantidade, m.data_movimentacao
        FROM movimentacoes m
        LEFT JOIN produtos p ON p.id = m.produto_id
        LEFT JOIN usuarios u ON u.id = m.usuario_id
        ORDER BY m.data_movimentacao DESC
    ''')
    rows = cursor.fetchall()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Produto', 'Usuário', 'Tipo', 'Quantidade', 'Data Movimentação'])
    for row in rows:
        writer.writerow([
            row['id'],
            row['produto'],
            row['usuario'],
            row['tipo'],
            row['quantidade'],
            row['data_movimentacao']
        ])
    return output.getvalue()


def export_produtos_pdf(conn):
    """Exporta produtos em PDF."""
    from fpdf import FPDF

    cursor = conn.cursor()
    cursor.execute('SELECT codigo, produto, categoria, estoque_atual, preco, status FROM produtos ORDER BY produto')
    rows = cursor.fetchall()
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, 'Relatório de Produtos', 0, 1, 'C')
    pdf.set_font('Helvetica', '', 11)
    pdf.ln(4)
    pdf.set_fill_color(15, 23, 42)
    pdf.set_text_color(255, 255, 255)
    headers = ['Código', 'Produto', 'Categoria', 'Estoque', 'Preço', 'Status']
    widths = [30, 80, 50, 25, 25, 70]
    for idx, header in enumerate(headers):
        pdf.cell(widths[idx], 10, header, 1, 0, 'C', True)
    pdf.ln()
    pdf.set_text_color(0, 0, 0)
    for row in rows:
        pdf.cell(widths[0], 8, str(row['codigo']), 1)
        pdf.cell(widths[1], 8, str(row['produto']), 1)
        pdf.cell(widths[2], 8, str(row['categoria']), 1)
        pdf.cell(widths[3], 8, str(row['estoque_atual']), 1)
        pdf.cell(widths[4], 8, f"R$ {row['preco']:.2f}", 1)
        pdf.cell(widths[5], 8, str(row['status']), 1)
        pdf.ln()
    return pdf.output(dest='S').encode('latin-1')


def export_movimentacoes_pdf(conn):
    """Exporta movimentações em PDF."""
    from fpdf import FPDF

    cursor = conn.cursor()
    cursor.execute('''
        SELECT m.id, p.produto AS produto, u.username AS usuario, m.tipo, m.quantidade, m.data_movimentacao
        FROM movimentacoes m
        LEFT JOIN produtos p ON p.id = m.produto_id
        LEFT JOIN usuarios u ON u.id = m.usuario_id
        ORDER BY m.data_movimentacao DESC
    ''')
    rows = cursor.fetchall()
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, 'Relatório de Movimentações', 0, 1, 'C')
    pdf.set_font('Helvetica', '', 11)
    pdf.ln(4)
    pdf.set_fill_color(15, 23, 42)
    pdf.set_text_color(255, 255, 255)
    headers = ['ID', 'Produto', 'Usuário', 'Tipo', 'Quantidade', 'Data']
    widths = [15, 80, 40, 30, 25, 60]
    for idx, header in enumerate(headers):
        pdf.cell(widths[idx], 10, header, 1, 0, 'C', True)
    pdf.ln()
    pdf.set_text_color(0, 0, 0)
    for row in rows:
        pdf.cell(widths[0], 8, str(row['id']), 1)
        pdf.cell(widths[1], 8, str(row['produto']), 1)
        pdf.cell(widths[2], 8, str(row['usuario']), 1)
        pdf.cell(widths[3], 8, str(row['tipo']), 1)
        pdf.cell(widths[4], 8, str(row['quantidade']), 1)
        pdf.cell(widths[5], 8, str(row['data_movimentacao']), 1)
        pdf.ln()
    return pdf.output(dest='S').encode('latin-1')


def export_produtos_xlsx(conn):
    """Exporta produtos em XLSX."""
    import io
    import xlsxwriter

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet('Produtos')
    headers = ['Código', 'Produto', 'Categoria', 'Estoque Atual', 'Estoque Mínimo', 'Preço', 'Status']
    for idx, header in enumerate(headers):
        worksheet.write(0, idx, header)

    cursor = conn.cursor()
    cursor.execute('SELECT codigo, produto, categoria, estoque_atual, estoque_minimo, preco, status FROM produtos ORDER BY produto')
    for row_index, row in enumerate(cursor.fetchall(), start=1):
        worksheet.write(row_index, 0, row['codigo'])
        worksheet.write(row_index, 1, row['produto'])
        worksheet.write(row_index, 2, row['categoria'])
        worksheet.write(row_index, 3, row['estoque_atual'])
        worksheet.write(row_index, 4, row['estoque_minimo'])
        worksheet.write(row_index, 5, row['preco'])
        worksheet.write(row_index, 6, row['status'])

    workbook.close()
    output.seek(0)
    return output.read()


def export_movimentacoes_xlsx(conn):
    """Exporta movimentações em XLSX."""
    import io
    import xlsxwriter

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet('Movimentacoes')
    headers = ['ID', 'Produto', 'Usuário', 'Tipo', 'Quantidade', 'Data Movimentacao']
    for idx, header in enumerate(headers):
        worksheet.write(0, idx, header)

    cursor = conn.cursor()
    cursor.execute('''
        SELECT m.id, p.produto AS produto, u.username AS usuario, m.tipo, m.quantidade, m.data_movimentacao
        FROM movimentacoes m
        LEFT JOIN produtos p ON p.id = m.produto_id
        LEFT JOIN usuarios u ON u.id = m.usuario_id
        ORDER BY m.data_movimentacao DESC
    ''')
    for row_index, row in enumerate(cursor.fetchall(), start=1):
        worksheet.write(row_index, 0, row['id'])
        worksheet.write(row_index, 1, row['produto'])
        worksheet.write(row_index, 2, row['usuario'])
        worksheet.write(row_index, 3, row['tipo'])
        worksheet.write(row_index, 4, row['quantidade'])
        worksheet.write(row_index, 5, row['data_movimentacao'])

    workbook.close()
    output.seek(0)
    return output.read()


def export_produtos_csv(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT codigo, produto, marca, categoria, estoque_atual, estoque_minimo, preco, status, criado_em FROM produtos ORDER BY produto')
    rows = cursor.fetchall()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Código', 'Produto', 'Marca', 'Categoria', 'Estoque Atual', 'Estoque Mínimo', 'Preço', 'Status', 'Criado em'])
    for row in rows:
        writer.writerow([
            row['codigo'],
            row['produto'],
            row['marca'],
            row['categoria'],
            row['estoque_atual'],
            row['estoque_minimo'],
            f"R$ {row['preco']:.2f}",
            row['status'],
            row['criado_em']
        ])
    return output.getvalue()


def export_movimentacoes_csv(conn):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT m.id, p.produto AS produto, u.username AS usuario, m.tipo, m.quantidade, m.data_movimentacao
        FROM movimentacoes m
        LEFT JOIN produtos p ON p.id = m.produto_id
        LEFT JOIN usuarios u ON u.id = m.usuario_id
        ORDER BY m.data_movimentacao DESC
    ''')
    rows = cursor.fetchall()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Produto', 'Usuário', 'Tipo', 'Quantidade', 'Data Movimentação'])
    for row in rows:
        writer.writerow([
            row['id'],
            row['produto'],
            row['usuario'],
            row['tipo'],
            row['quantidade'],
            row['data_movimentacao']
        ])
    return output.getvalue()


def export_produtos_pdf(conn):
    from fpdf import FPDF

    cursor = conn.cursor()
    cursor.execute('SELECT codigo, produto, categoria, estoque_atual, preco, status FROM produtos ORDER BY produto')
    rows = cursor.fetchall()
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, 'Relatório de Produtos', 0, 1, 'C')
    pdf.set_font('Helvetica', '', 11)
    pdf.ln(4)
    pdf.set_fill_color(15, 23, 42)
    pdf.set_text_color(255, 255, 255)
    headers = ['Código', 'Produto', 'Categoria', 'Estoque', 'Preço', 'Status']
    widths = [30, 80, 50, 25, 25, 70]
    for idx, header in enumerate(headers):
        pdf.cell(widths[idx], 10, header, 1, 0, 'C', True)
    pdf.ln()
    pdf.set_text_color(0, 0, 0)
    for row in rows:
        pdf.cell(widths[0], 8, str(row['codigo']), 1)
        pdf.cell(widths[1], 8, str(row['produto']), 1)
        pdf.cell(widths[2], 8, str(row['categoria']), 1)
        pdf.cell(widths[3], 8, str(row['estoque_atual']), 1)
        pdf.cell(widths[4], 8, f"R$ {row['preco']:.2f}", 1)
        pdf.cell(widths[5], 8, str(row['status']), 1)
        pdf.ln()
    return pdf.output(dest='S').encode('latin-1')


def export_movimentacoes_pdf(conn):
    from fpdf import FPDF

    cursor = conn.cursor()
    cursor.execute('''
        SELECT m.id, p.produto AS produto, u.username AS usuario, m.tipo, m.quantidade, m.data_movimentacao
        FROM movimentacoes m
        LEFT JOIN produtos p ON p.id = m.produto_id
        LEFT JOIN usuarios u ON u.id = m.usuario_id
        ORDER BY m.data_movimentacao DESC
    ''')
    rows = cursor.fetchall()
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, 'Relatório de Movimentações', 0, 1, 'C')
    pdf.set_font('Helvetica', '', 11)
    pdf.ln(4)
    pdf.set_fill_color(15, 23, 42)
    pdf.set_text_color(255, 255, 255)
    headers = ['ID', 'Produto', 'Usuário', 'Tipo', 'Quantidade', 'Data']
    widths = [15, 80, 40, 30, 25, 60]
    for idx, header in enumerate(headers):
        pdf.cell(widths[idx], 10, header, 1, 0, 'C', True)
    pdf.ln()
    pdf.set_text_color(0, 0, 0)
    for row in rows:
        pdf.cell(widths[0], 8, str(row['id']), 1)
        pdf.cell(widths[1], 8, str(row['produto']), 1)
        pdf.cell(widths[2], 8, str(row['usuario']), 1)
        pdf.cell(widths[3], 8, str(row['tipo']), 1)
        pdf.cell(widths[4], 8, str(row['quantidade']), 1)
        pdf.cell(widths[5], 8, str(row['data_movimentacao']), 1)
        pdf.ln()
    return pdf.output(dest='S').encode('latin-1')


def export_produtos_xlsx(conn):
    import io
    import xlsxwriter

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet('Produtos')
    headers = ['Código', 'Produto', 'Categoria', 'Estoque Atual', 'Estoque Mínimo', 'Preço', 'Status']
    for idx, header in enumerate(headers):
        worksheet.write(0, idx, header)

    cursor = conn.cursor()
    cursor.execute('SELECT codigo, produto, categoria, estoque_atual, estoque_minimo, preco, status FROM produtos ORDER BY produto')
    for row_index, row in enumerate(cursor.fetchall(), start=1):
        worksheet.write(row_index, 0, row['codigo'])
        worksheet.write(row_index, 1, row['produto'])
        worksheet.write(row_index, 2, row['categoria'])
        worksheet.write(row_index, 3, row['estoque_atual'])
        worksheet.write(row_index, 4, row['estoque_minimo'])
        worksheet.write(row_index, 5, row['preco'])
        worksheet.write(row_index, 6, row['status'])

    workbook.close()
    output.seek(0)
    return output.read()


def export_movimentacoes_xlsx(conn):
    import io
    import xlsxwriter

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet('Movimentacoes')
    headers = ['ID', 'Produto', 'Usuário', 'Tipo', 'Quantidade', 'Data Movimentacao']
    for idx, header in enumerate(headers):
        worksheet.write(0, idx, header)

    cursor = conn.cursor()
    cursor.execute('''
        SELECT m.id, p.produto AS produto, u.username AS usuario, m.tipo, m.quantidade, m.data_movimentacao
        FROM movimentacoes m
        LEFT JOIN produtos p ON p.id = m.produto_id
        LEFT JOIN usuarios u ON u.id = m.usuario_id
        ORDER BY m.data_movimentacao DESC
    ''')
    for row_index, row in enumerate(cursor.fetchall(), start=1):
        worksheet.write(row_index, 0, row['id'])
        worksheet.write(row_index, 1, row['produto'])
        worksheet.write(row_index, 2, row['usuario'])
        worksheet.write(row_index, 3, row['tipo'])
        worksheet.write(row_index, 4, row['quantidade'])
        worksheet.write(row_index, 5, row['data_movimentacao'])

    workbook.close()
    output.seek(0)
    return output.read()
