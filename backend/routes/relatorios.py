from flask import Blueprint, jsonify, Response, request
from flask_jwt_extended import jwt_required
from datetime import datetime
from backend.database.db import conectar_banco
from backend.services.report_service import (
    dashboard_resumo,
    categorias_por_produto,
    movimentacoes_por_tipo,
    relatorio_periodo,
    produtos_mais_movimentados,
    estatisticas_estoque,
    valor_total_estoque_por_categoria,
    export_produtos_csv,
    export_movimentacoes_csv,
    export_produtos_pdf,
    export_movimentacoes_pdf,
    export_produtos_xlsx,
    export_movimentacoes_xlsx,
)

relatorios_bp = Blueprint('relatorios', __name__)


@relatorios_bp.route('/relatorios/resumo', methods=['GET'])
def resumo():
    """Retorna resumo do dashboard."""
    with conectar_banco() as conn:
        data = dashboard_resumo(conn)
    return jsonify(data)


@relatorios_bp.route('/grafico/categorias', methods=['GET'])
def grafico_categorias():
    """Retorna dados para gráfico de produtos por categoria."""
    with conectar_banco() as conn:
        data = categorias_por_produto(conn)
    return jsonify([{'categoria': row['categoria'], 'total': row['total']} for row in data])


@relatorios_bp.route('/grafico/movimentacoes', methods=['GET'])
def grafico_movimentacoes():
    """Retorna dados para gráfico de movimentações por tipo."""
    with conectar_banco() as conn:
        data = movimentacoes_por_tipo(conn)
    return jsonify([{'tipo': row['tipo'], 'total': row['total']} for row in data])


@relatorios_bp.route('/relatorios/periodo', methods=['GET'])
def periodo():
    """Retorna movimentações de um período."""
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    if not data_inicio or not data_fim:
        return jsonify({'erro': 'data_inicio e data_fim são obrigatórios'}), 400
    
    try:
        with conectar_banco() as conn:
            data = relatorio_periodo(conn, data_inicio, data_fim)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@relatorios_bp.route('/relatorios/mais-movimentados', methods=['GET'])
def mais_movimentados():
    """Retorna produtos mais movimentados."""
    limite = request.args.get('limite', 10, type=int)
    with conectar_banco() as conn:
        data = produtos_mais_movimentados(conn, limite)
    return jsonify(data), 200


@relatorios_bp.route('/relatorios/estatisticas-estoque', methods=['GET'])
def stat_estoque():
    """Retorna estatísticas de estoque."""
    with conectar_banco() as conn:
        data = estatisticas_estoque(conn)
    return jsonify(data), 200


@relatorios_bp.route('/relatorios/valor-categoria', methods=['GET'])
def valor_categoria():
    """Retorna valor total do estoque por categoria."""
    with conectar_banco() as conn:
        data = valor_total_estoque_por_categoria(conn)
    return jsonify(data), 200


@relatorios_bp.route('/relatorios/produtos/csv', methods=['GET'])
@jwt_required()
def exportar_produtos_csv():
    """Exporta produtos em CSV."""
    with conectar_banco() as conn:
        csv_data = export_produtos_csv(conn)
    timestamp = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
    return Response(csv_data, mimetype='text/csv', headers={
        'Content-Disposition': f'attachment; filename=produtos_{timestamp}.csv'
    })


@relatorios_bp.route('/relatorios/movimentacoes/csv', methods=['GET'])
@jwt_required()
def exportar_movimentacoes_csv():
    """Exporta movimentações em CSV."""
    with conectar_banco() as conn:
        csv_data = export_movimentacoes_csv(conn)
    timestamp = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
    return Response(csv_data, mimetype='text/csv', headers={
        'Content-Disposition': f'attachment; filename=movimentacoes_{timestamp}.csv'
    })


@relatorios_bp.route('/relatorios/produtos/pdf', methods=['GET'])
@jwt_required()
def exportar_produtos_pdf():
    """Exporta produtos em PDF."""
    with conectar_banco() as conn:
        pdf_data = export_produtos_pdf(conn)
    timestamp = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
    return Response(pdf_data, mimetype='application/pdf', headers={
        'Content-Disposition': f'attachment; filename=produtos_{timestamp}.pdf'
    })


@relatorios_bp.route('/relatorios/movimentacoes/pdf', methods=['GET'])
@jwt_required()
def exportar_movimentacoes_pdf():
    """Exporta movimentações em PDF."""
    with conectar_banco() as conn:
        pdf_data = export_movimentacoes_pdf(conn)
    timestamp = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
    return Response(pdf_data, mimetype='application/pdf', headers={
        'Content-Disposition': f'attachment; filename=movimentacoes_{timestamp}.pdf'
    })


@relatorios_bp.route('/relatorios/produtos/xlsx', methods=['GET'])
@jwt_required()
def exportar_produtos_xlsx():
    """Exporta produtos em XLSX."""
    with conectar_banco() as conn:
        xlsx_data = export_produtos_xlsx(conn)
    timestamp = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
    return Response(xlsx_data, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', headers={
        'Content-Disposition': f'attachment; filename=produtos_{timestamp}.xlsx'
    })


@relatorios_bp.route('/relatorios/movimentacoes/xlsx', methods=['GET'])
@jwt_required()
def exportar_movimentacoes_xlsx():
    """Exporta movimentações em XLSX."""
    with conectar_banco() as conn:
        xlsx_data = export_movimentacoes_xlsx(conn)
    timestamp = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
    return Response(xlsx_data, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', headers={
        'Content-Disposition': f'attachment; filename=movimentacoes_{timestamp}.xlsx'
    })
