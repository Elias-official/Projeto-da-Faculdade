import { useEffect, useState } from 'react'

import {

    PieChart,
    Pie,
    Cell,
    Tooltip,
    ResponsiveContainer

} from 'recharts'

import API_URL from '../services/api'

function Grafico() {

    const [dados, setDados] = useState([])

    useEffect(() => {

        buscarDados()

    }, [])

    async function buscarDados() {

        const response = await fetch(
            `${API_URL}/grafico/categorias`
        )

        const data = await response.json()

        setDados(data)
    }

    const COLORS = [

        '#0088FE',
        '#00C49F',
        '#FFBB28',
        '#FF8042',
        '#845EC2',
        '#D65DB1'
    ]

    return (

        <div className="chart-box">

            <h2>Produtos por Categoria</h2>

            <div style={{
                width: '100%',
                height: '300px'
            }}>

                <ResponsiveContainer>

                    <PieChart>

                        <Pie

                            data={dados}

                            dataKey="total"

                            nameKey="categoria"

                            outerRadius={100}

                            label
                        >

                            {dados.map((entry, index) => (

                                <Cell
                                    key={index}

                                    fill={
                                        COLORS[
                                            index % COLORS.length
                                        ]
                                    }
                                />

                            ))}

                        </Pie>

                        <Tooltip />

                    </PieChart>

                </ResponsiveContainer>

            </div>

        </div>
    )
}

// styling via global.css

export default Grafico