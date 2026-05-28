import { useEffect, useRef, useState } from 'react'
import { createPortal } from 'react-dom'
import { api } from '../services/api'
import { BellRing, AlertTriangle, Activity } from 'lucide-react'

function NotificationPanel({ open, onClose }) {
  const [produtos, setProdutos] = useState([])
  const [movimentacoes, setMovimentacoes] = useState([])
  const panelRef = useRef(null)
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  useEffect(() => {
    if (!open) {
      return
    }

    buscarAlertas()
    buscarMovimentacoes()

    function handleClickOutside(event) {
      if (panelRef.current && !panelRef.current.contains(event.target)) {
        onClose?.()
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [open, onClose])

  async function buscarAlertas() {
    try {
      const response = await api.get('/produtos')
      setProdutos(response.data.filter((item) => item.status !== 'Estoque normal').slice(0, 4))
    } catch (error) {
      console.error(error)
    }
  }

  async function buscarMovimentacoes() {
    try {
      const response = await api.get('/movimentacoes')
      setMovimentacoes(response.data.slice(0, 4))
    } catch (error) {
      console.error(error)
    }
  }

  if (!open || !mounted) {
    return null
  }

  const panel = (
    <div ref={panelRef} className="glass-card fixed right-6 top-24 w-full max-w-sm rounded-[2rem] border border-slate-800 bg-slate-950/95 p-6 shadow-soft backdrop-blur-xl" style={{ zIndex: 9999 }}>
      <div className="flex items-center justify-between gap-3">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-slate-400">Notificações</p>
          <h2 className="mt-2 text-xl font-semibold text-slate-100">Atualizações do estoque</h2>
        </div>
        <BellRing className="text-blue-400" size={22} />
      </div>
      <div className="mt-6 space-y-5">
        <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-4 shadow-soft">
          <p className="text-sm text-slate-400">Produtos críticos</p>
          {produtos.length === 0 ? (
            <p className="mt-3 text-slate-500">Nenhum alerta no momento.</p>
          ) : (
            produtos.map((produto) => (
              <div key={produto.id} className="mt-3 rounded-3xl bg-slate-950/80 p-3">
                <div className="flex items-center justify-between gap-3">
                  <div>
                    <p className="font-semibold text-slate-100">{produto.produto}</p>
                    <p className="text-sm text-slate-400">{produto.status}</p>
                  </div>
                  {(() => {
                    const isAttention = produto.status?.toLowerCase().includes('atenção')
                    return (
                      <span className={`inline-flex items-center gap-1 rounded-full px-3 py-1 text-xs font-semibold ${isAttention ? 'bg-amber-500/15 text-amber-300' : 'bg-red-500/15 text-red-300'}`}>
                        <AlertTriangle size={12} /> {isAttention ? 'Atenção' : 'Crítico'}
                      </span>
                    )
                  })()}
                </div>
              </div>
            ))
          )}
        </div>
        <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-4 shadow-soft">
          <div className="flex items-center gap-2 text-slate-300">
            <Activity size={18} />
            <p className="text-sm">Últimas movimentações</p>
          </div>
          <div className="mt-4 space-y-3">
            {movimentacoes.length === 0 ? (
              <p className="text-slate-500">Sem movimentações recentes.</p>
            ) : (
              movimentacoes.map((mov) => (
                <div key={mov.id} className="rounded-3xl bg-slate-950/80 p-3">
                  <div className="flex items-center justify-between gap-3">
                    <div className="text-sm text-slate-300">{mov.produto || 'Produto removido'}</div>
                    <span className="rounded-full bg-slate-800 px-3 py-1 text-xs text-slate-300">{mov.tipo}</span>
                  </div>
                  <div className="mt-2 flex items-center justify-between text-xs text-slate-500">
                    <span>Qtd {mov.quantidade}</span>
                    <span>{new Date(mov.data_movimentacao).toLocaleDateString('pt-BR')}</span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  )

  return createPortal(panel, document.body)
}

export default NotificationPanel
