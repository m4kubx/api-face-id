'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'

interface User {
  id: string
  username: string
  email: string
  role: string
}

interface Face {
  id: string
  user_id: string
  image_url: string
  created_at: string
}

export default function Dashboard() {
  const [user, setUser] = useState<User | null>(null)
  const [faces, setFaces] = useState<Face[]>([])
  const [loading, setLoading] = useState(true)
  const [uploading, setUploading] = useState(false)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [verifyResult, setVerifyResult] = useState<any>(null)
  const [activeTab, setActiveTab] = useState<'faces' | 'verify'>('faces')
  const router = useRouter()

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/')
      return
    }
    fetchUser()
    fetchFaces()
  }, [])

  const fetchUser = async () => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/auth/me`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      })
      if (res.ok) {
        setUser(await res.json())
      }
    } catch (err) {
      console.error(err)
    }
  }

  const fetchFaces = async () => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/faces/list`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      })
      if (res.ok) {
        setFaces(await res.json())
      }
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleUpload = async () => {
    if (!selectedFile) return
    setUploading(true)

    const formData = new FormData()
    formData.append('file', selectedFile)

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/faces/register?user_id=${user?.id}`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
        body: formData
      })

      if (res.ok) {
        setSelectedFile(null)
        fetchFaces()
      }
    } catch (err) {
      console.error(err)
    } finally {
      setUploading(false)
    }
  }

  const handleVerify = async () => {
    if (!selectedFile) return
    setUploading(true)

    const formData = new FormData()
    formData.append('file', selectedFile)

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/verify/identify`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
        body: formData
      })

      if (res.ok) {
        setVerifyResult(await res.json())
      }
    } catch (err) {
      console.error(err)
    } finally {
      setUploading(false)
    }
  }

  const handleDelete = async (faceId: string) => {
    if (!confirm('¿Eliminar este rostro registrado?')) return

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/faces/${faceId}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      })

      if (res.ok) {
        fetchFaces()
      }
    } catch (err) {
      console.error(err)
    }
  }

  const handleLogout = () => {
    localStorage.clear()
    router.push('/')
  }

  return (
    <div className="min-h-screen bg-gray-900">
      <nav className="bg-gray-800 border-b border-gray-700">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
            </div>
            <span className="text-white font-semibold">Face ID Dashboard</span>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-gray-400 text-sm">{user?.email}</span>
            <button
              onClick={handleLogout}
              className="text-gray-400 hover:text-white text-sm"
            >
              Cerrar Sesión
            </button>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="flex gap-4 mb-8">
          <button
            onClick={() => setActiveTab('faces')}
            className={`px-4 py-2 rounded-lg ${activeTab === 'faces' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300'}`}
          >
            Rostros Registrados ({faces.length})
          </button>
          <button
            onClick={() => setActiveTab('verify')}
            className={`px-4 py-2 rounded-lg ${activeTab === 'verify' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300'}`}
          >
            Verificar Rostro
          </button>
        </div>

        {activeTab === 'faces' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="bg-gray-800 rounded-xl p-6">
              <h3 className="text-white text-lg font-semibold mb-4">Registrar Nuevo Rostro</h3>
              <div className="space-y-4">
                <input
                  type="file"
                  accept="image/*"
                  onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
                  className="w-full text-gray-300 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-blue-600 file:text-white hover:file:bg-blue-700"
                />
                <button
                  onClick={handleUpload}
                  disabled={!selectedFile || uploading}
                  className="w-full py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white rounded-lg transition-colors"
                >
                  {uploading ? 'Subiendo...' : 'Registrar Rostro'}
                </button>
              </div>
            </div>

            <div className="bg-gray-800 rounded-xl p-6">
              <h3 className="text-white text-lg font-semibold mb-4">Rostros Registrados</h3>
              {loading ? (
                <p className="text-gray-400">Cargando...</p>
              ) : faces.length === 0 ? (
                <p className="text-gray-400">No hay rostros registrados</p>
              ) : (
                <div className="space-y-3 max-h-96 overflow-y-auto">
                  {faces.map((face) => (
                    <div key={face.id} className="flex items-center justify-between bg-gray-700/50 rounded-lg p-3">
                      <div>
                        <p className="text-white text-sm">ID: {face.user_id.slice(0, 8)}...</p>
                        <p className="text-gray-400 text-xs">{new Date(face.created_at).toLocaleDateString()}</p>
                      </div>
                      <button
                        onClick={() => handleDelete(face.id)}
                        className="text-red-400 hover:text-red-300 text-sm"
                      >
                        Eliminar
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'verify' && (
          <div className="max-w-xl mx-auto">
            <div className="bg-gray-800 rounded-xl p-6">
              <h3 className="text-white text-lg font-semibold mb-4">Verificar Identidad</h3>
              <div className="space-y-4">
                <input
                  type="file"
                  accept="image/*"
                  onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
                  className="w-full text-gray-300 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-blue-600 file:text-white hover:file:bg-blue-700"
                />
                <button
                  onClick={handleVerify}
                  disabled={!selectedFile || uploading}
                  className="w-full py-3 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 text-white rounded-lg transition-colors"
                >
                  {uploading ? 'Verificando...' : 'Verificar Rostro'}
                </button>

                {verifyResult && (
                  <div className={`mt-4 p-4 rounded-lg ${verifyResult.identified ? 'bg-green-500/20 border border-green-500/50' : 'bg-red-500/20 border border-red-500/50'}`}>
                    <p className={`font-semibold ${verifyResult.identified ? 'text-green-400' : 'text-red-400'}`}>
                      {verifyResult.identified ? 'IDENTIFICADO' : 'NO IDENTIFICADO'}
                    </p>
                    {verifyResult.identified && (
                      <>
                        <p className="text-gray-300 text-sm mt-1">User ID: {verifyResult.user_id}</p>
                        <p className="text-gray-300 text-sm">Confianza: {(verifyResult.confidence * 100).toFixed(1)}%</p>
                      </>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
