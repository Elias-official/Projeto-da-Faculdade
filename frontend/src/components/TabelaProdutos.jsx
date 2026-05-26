function TabelaProdutos({ produtos, loading, onEdit, onDelete }) {
  if (loading) {
    return <div className="py-8 text-center text-slate-400">Carregando produtos...</div>
  }

  if (produtos.length === 0) {
    return <div className="py-8 text-center text-slate-400">Nenhum produto encontrado.</div>
  }

  return (
    <div className="overflow-hidden rounded-3xl border border-slate-800 bg-slate-950/90 shadow-soft">
      <table className="min-w-full border-separate border-spacing-0 text-left">
        <thead className="bg-slate-900 text-slate-400">
          <tr>
            <th className="px-5 py-4">Código</th>
            <th className="px-5 py-4">Produto</th>
            <th className="px-5 py-4">Categoria</th>
            <th className="px-5 py-4">Estoque</th>
            <th className="px-5 py-4">Status</th>
            <th className="px-5 py-4">Ações</th>
          </tr>
        </thead>
        <tbody>
          {produtos.map((produto) => (
            <tr key={produto.id} className="border-t border-slate-800/70 hover:bg-slate-900">
              <td className="px-5 py-4 text-slate-200">{produto.codigo}</td>
              <td className="px-5 py-4 text-slate-100">{produto.produto}</td>
              <td className="px-5 py-4 text-slate-300">{produto.categoria}</td>
              <td className="px-5 py-4 text-slate-100">{produto.estoque_atual}</td>
              <td className="px-5 py-4">
                <span
                  className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ${
                    produto.status.includes('Crítico')
                      ? 'bg-red-500/15 text-red-300'
                      : produto.status.includes('Atenção')
                      ? 'bg-yellow-500/15 text-yellow-300'
                      : produto.status.includes('Sem estoque')
                      ? 'bg-red-500/15 text-red-300'
                      : 'bg-emerald-500/15 text-emerald-300'
                  }`}
                >
                  {produto.status}
                </span>
              </td>
              <td className="px-5 py-4">
                <div className="flex flex-wrap gap-2">
                  <button
                    onClick={() => onEdit(produto)}
                    className="rounded-2xl bg-blue-600 px-3 py-2 text-xs font-semibold text-white transition hover:bg-blue-500"
                  >
                    Editar
                  </button>
                  <button
                    onClick={() => onDelete(produto.id)}
                    className="rounded-2xl bg-red-500 px-3 py-2 text-xs font-semibold text-white transition hover:bg-red-400"
                  >
                    Excluir
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default TabelaProdutos
