import { useState } from 'react'

import API_URL from '../services/api'

function Login() {

    const [usuario, setUsuario] = useState('')

    const [senha, setSenha] = useState('')

    async function fazerLogin(e) {

        e.preventDefault()

        const response = await fetch(
            `${API_URL}/login`,
            {
                method: 'POST',

                headers: {
                    'Content-Type': 'application/json'
                },

                body: JSON.stringify({
                    username: usuario,
                    senha
                })
            }
        )

        const data = await response.json()

        if (data.token) {

            localStorage.setItem(
                'token',
                data.token
            )

            window.location.href = '/dashboard'

        } else {

            alert(data.erro)
        }
    }

    return (

        <div style={container}>

            <form
                onSubmit={fazerLogin}
                style={box}
            >

                <h1>Login</h1>

                <input
                    type="text"
                    placeholder="Usuário"
                    value={usuario}
                    onChange={(e) =>
                        setUsuario(e.target.value)
                    }
                />

                <input
                    type="password"
                    placeholder="Senha"
                    value={senha}
                    onChange={(e) =>
                        setSenha(e.target.value)
                    }
                />

                <button type="submit">

                    Entrar

                </button>

            </form>

        </div>
    )
}

const container = {

    height: '100vh',

    display: 'flex',

    justifyContent: 'center',

    alignItems: 'center',

    background: '#f5f6fa'
}

const box = {

    background: 'white',

    padding: '40px',

    borderRadius: '12px',

    display: 'flex',

    flexDirection: 'column',

    gap: '15px',

    width: '300px'
}

export default Login