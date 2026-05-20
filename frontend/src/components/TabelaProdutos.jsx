import { useEffect, useState } from 'react'
import API_URL from '../services/api'

function TabelaProdutos() {

    const [produtos, setProdutos] = useState([])

    useEffect(() => {

        buscarProdutos()

    }, [])

    async function buscarProdutos() {

        const response = await fetch(`${API_URL}/produtos`)

        const data = await response.json()

        setProdutos(data)
    }

    return (

        <div className="table-box">

            <h2>Produtos</h2>

            <table>

                <thead>

                    <tr>

                        <th>Produto</th>
                        <th>Categoria</th>
                        <th>Estoque</th>
                        <th>Status</th>

                    </tr>

                </thead>

                <tbody>

                    {produtos.map(produto => (

                        <tr key={produto.id}>

                            <td>{produto.produto}</td>

                            <td>{produto.categoria}</td>

                            <td>{produto.estoque_atual}</td>

                            <td>{produto.status}</td>

                        </tr>

                    ))}

                </tbody>

            </table>

        </div>
    )
}

// styling via global.css

export default TabelaProdutos