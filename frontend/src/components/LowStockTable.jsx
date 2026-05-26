function LowStockTable({ produtos }) {
  return (
    <div className="glass-card p-6">
      <div className="flex items-center justify-between gap-3">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-slate-400">Produtos com estoque baixo</p>
          <h2 className="mt-2 text-2xl font-semibold text-slate-100">Requer atenção</h2>
        </div>
      </div>
      <div className="mt-6 overflow-x-auto">
        <table className="min-w-full border-separate border-spacing-0 text-left">
          <thead className="bg-slate-900 text-slate-400">
            <tr>
              <th className="px-4 py-3">Produto</th>
              <th className="px-4 py-3">Categoria</th>
              <th className="px-4 py-3">Estoque atual</th>
              <th className="px-4 py-3">Mínimo</th>
              <th className="px-4 py-3">Status</th>
            </tr>
          </thead>
          <tbody>
            {produtos.map((produto) => (
              <tr key={produto.id} className="border-t border-slate-800/70 hover:bg-slate-900">
                <td className="px-4 py-3 text-slate-100">{produto.produto}</td>
                <td className="px-4 py-3 text-slate-300">{produto.categoria}</td>
                <td className="px-4 py-3 text-slate-100">{produto.estoque_atual}</td>
                <td className="px-4 py-3 text-slate-300">{produto.estoque_minimo ?? '-'}</td>
                <td className="px-4 py-3">
                  <span className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ${produto.status.includes('Crítico') ? 'bg-red-500/15 text-red-300' : 'bg-yellow-500/15 text-yellow-300'}`}>
                    {produto.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default LowStockTable
