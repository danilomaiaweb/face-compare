import React, { useState, useRef, useEffect } from 'react';
import "./App.css";
import axios from "axios";
import { Button } from "./components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "./components/ui/card";
import { Progress } from "./components/ui/progress";
import { Alert, AlertDescription } from "./components/ui/alert";
import { Badge } from "./components/ui/badge";
import { Upload, Camera, RotateCcw, CheckCircle, AlertCircle, Loader2 } from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function App() {
  const [baseImage, setBaseImage] = useState(null);
  const [baseImagePreview, setBaseImagePreview] = useState(null);
  const [comparisonImages, setComparisonImages] = useState([]);
  const [comparisonPreviews, setComparisonPreviews] = useState([]);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loginPassword, setLoginPassword] = useState('');
  const [loginError, setLoginError] = useState('');

  const baseImageRef = useRef(null);
  const comparisonImagesRef = useRef(null);

  // Simple authentication - In production, this should be more secure
  const VALID_PASSWORD = 'painho123'; // Change this to your desired password

  const handleLogin = (e) => {
    e.preventDefault();
    if (loginPassword === VALID_PASSWORD) {
      setIsAuthenticated(true);
      setLoginError('');
      localStorage.setItem('auth_token', 'authenticated'); // Simple session storage
    } else {
      setLoginError('Senha incorreta. Tente novamente.');
      setLoginPassword('');
    }
  };

  // Check if user was previously authenticated
  useEffect(() => {
    const token = localStorage.getItem('auth_token');
    if (token === 'authenticated') {
      setIsAuthenticated(true);
    }

    // Remove any Emergent branding dynamically
    const removeEmergentElements = () => {
      try {
        const elementsToRemove = [
          ...document.querySelectorAll('[data-testid="made-with-emergent"]'),
          ...document.querySelectorAll('*[href*="emergent"]'),
          ...document.querySelectorAll('*[class*="emergent"]'),
          ...document.querySelectorAll('*[id*="emergent"]'),
          ...Array.from(document.querySelectorAll('*')).filter(el => 
            el.textContent && el.textContent.toLowerCase().includes('made with emergent')
          ),
          ...Array.from(document.querySelectorAll('div')).filter(el => {
            try {
              const style = window.getComputedStyle(el);
              return style.position === 'fixed' && 
                     (style.bottom !== 'auto' || style.right !== 'auto');
            } catch (e) {
              return false;
            }
          })
        ];

        elementsToRemove.forEach(el => {
          try {
            if (el && el.parentNode) {
              el.remove();
            }
          } catch (e) {
            // Ignore removal errors
          }
        });
      } catch (e) {
        // Ignore any errors in element removal
      }
    };

    // Remove on load with delay to ensure DOM is ready
    const timeoutId = setTimeout(removeEmergentElements, 100);

    // Set up observer for dynamic content only if document.body exists
    let observer = null;
    if (document.body) {
      try {
        observer = new MutationObserver(removeEmergentElements);
        observer.observe(document.body, {
          childList: true,
          subtree: true
        });
      } catch (e) {
        // Ignore observer setup errors
      }
    }

    // Cleanup observer and timeout
    return () => {
      clearTimeout(timeoutId);
      if (observer) {
        try {
          observer.disconnect();
        } catch (e) {
          // Ignore disconnect errors
        }
      }
    };
  }, []);

  const handleLogout = () => {
    setIsAuthenticated(false);
    localStorage.removeItem('auth_token');
    // Reset all states
    setBaseImage(null);
    setBaseImagePreview(null);
    setComparisonImages([]);
    setComparisonPreviews([]);
    setResults(null);
    setError(null);
  };

  // Login Screen Component
  const LoginScreen = () => (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black flex items-center justify-center">
      <Card className="w-full max-w-md border-gray-600 bg-gray-800/90 backdrop-blur-sm shadow-2xl">
        <CardHeader className="text-center">
          <div className="flex justify-center mb-4">
            <div className="p-3 bg-blue-600 rounded-lg">
              <Camera className="h-8 w-8 text-white" />
            </div>
          </div>
          <CardTitle className="text-2xl text-white">Comparador Facial Painho Trampos</CardTitle>
          <p className="text-gray-400 mt-2">Acesso Restrito - Digite a senha para continuar</p>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-300 mb-2">
                Senha de Acesso
              </label>
              <input
                type="password"
                id="password"
                value={loginPassword}
                onChange={(e) => setLoginPassword(e.target.value)}
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Digite sua senha"
                required
              />
            </div>
            
            {loginError && (
              <Alert className="border-red-500 bg-red-900/50">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription className="text-red-400">
                  {loginError}
                </AlertDescription>
              </Alert>
            )}
            
            <Button 
              type="submit" 
              className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white py-2 px-4 rounded-lg transition-all duration-200"
            >
              Entrar
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );

  // If not authenticated, show login screen
  if (!isAuthenticated) {
    return <LoginScreen />;
  }

  const handleBaseImageChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      // Validate file type
      if (!file.type.startsWith('image/')) {
        setError('Por favor, selecione apenas arquivos de imagem.');
        return;
      }
      
      // Validate file size (max 10MB)
      if (file.size > 10 * 1024 * 1024) {
        setError('A imagem deve ter no máximo 10MB.');
        return;
      }

      setBaseImage(file);
      setError(null);
      
      // Create preview
      const reader = new FileReader();
      reader.onload = (e) => {
        setBaseImagePreview(e.target.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleComparisonImagesChange = (event) => {
    const files = Array.from(event.target.files);
    
    // Validate file count
    if (files.length > 250) {
      setError('Máximo de 250 imagens permitido.');
      return;
    }
    
    // Validate file types and sizes
    const validFiles = [];
    const previews = [];
    
    for (const file of files) {
      if (!file.type.startsWith('image/')) {
        setError('Todos os arquivos devem ser imagens.');
        return;
      }
      
      if (file.size > 10 * 1024 * 1024) {
        setError('Cada imagem deve ter no máximo 10MB.');
        return;
      }
      
      validFiles.push(file);
      
      // Create preview
      const reader = new FileReader();
      reader.onload = (e) => {
        previews.push({
          id: file.name,
          url: e.target.result,
          name: file.name
        });
        
        if (previews.length === validFiles.length) {
          setComparisonPreviews(previews);
        }
      };
      reader.readAsDataURL(file);
    }
    
    setComparisonImages(validFiles);
    setError(null);
  };

  const handleSubmit = async () => {
    if (!baseImage) {
      setError('Por favor, selecione uma imagem base.');
      return;
    }
    
    if (comparisonImages.length === 0) {
      setError('Por favor, selecione pelo menos uma imagem para comparação.');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);
    setUploadProgress(0);

    try {
      const formData = new FormData();
      formData.append('base_image', baseImage);
      
      comparisonImages.forEach((file) => {
        formData.append('comparison_images', file);
      });

      const response = await axios.post(`${API}/compare-faces`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          setUploadProgress(percentCompleted);
        },
      });

      setResults(response.data);
      
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Erro ao processar as imagens. Tente novamente.';
      setError(errorMessage);
    } finally {
      setLoading(false);
      setUploadProgress(0);
    }
  };

  const resetForm = () => {
    setBaseImage(null);
    setBaseImagePreview(null);
    setComparisonImages([]);
    setComparisonPreviews([]);
    setResults(null);
    setError(null);
    setUploadProgress(0);
    
    if (baseImageRef.current) baseImageRef.current.value = '';
    if (comparisonImagesRef.current) comparisonImagesRef.current.value = '';
  };

  const getColorForSimilarity = (similarity) => {
    if (similarity >= 80) return 'bg-emerald-500';
    if (similarity >= 60) return 'bg-amber-500';
    if (similarity >= 40) return 'bg-orange-500';
    return 'bg-red-500';
  };

  const getSimilarityLabel = (similarity) => {
    if (similarity >= 80) return 'Alta';
    if (similarity >= 60) return 'Média';
    if (similarity >= 40) return 'Baixa';
    return 'Muito Baixa';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black flex flex-col">
      {/* Header */}
      <header className="bg-gray-900/90 backdrop-blur-sm shadow-sm border-b border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-blue-600 rounded-lg">
                <Camera className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-white">Comparador Facial Painho Trampos</h1>
                <p className="text-gray-300 mt-1">Compare rostos e descubra similaridades com precisão</p>
              </div>
            </div>
            <Button 
              onClick={handleLogout}
              variant="outline"
              className="border-gray-600 text-gray-300 hover:bg-gray-700 hover:text-white"
            >
              Sair
            </Button>
          </div>
        </div>
      </header>

      <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full">
        {/* Upload Section */}
        <div className="grid md:grid-cols-2 gap-8 mb-8">
          {/* Base Image Upload */}
          <Card className="border-gray-600 shadow-lg bg-gray-800/70 backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-blue-400">
                <Upload className="h-5 w-5" />
                Imagem Base
              </CardTitle>
              <p className="text-sm text-gray-400">
                Faça upload da imagem principal com o rosto de referência
              </p>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="border-2 border-dashed border-blue-500 rounded-lg p-6 text-center hover:border-blue-400 transition-colors bg-gray-900/50">
                  <input
                    type="file"
                    ref={baseImageRef}
                    onChange={handleBaseImageChange}
                    accept="image/*"
                    className="hidden"
                    id="base-image"
                  />
                  <label htmlFor="base-image" className="cursor-pointer">
                    {baseImagePreview ? (
                      <div className="space-y-3">
                        <img
                          src={baseImagePreview}
                          alt="Preview"
                          className="mx-auto max-h-48 rounded-lg shadow-md"
                        />
                        <p className="text-sm text-green-400 font-medium">
                          ✓ Imagem carregada com sucesso
                        </p>
                      </div>
                    ) : (
                      <div className="space-y-3">
                        <Upload className="mx-auto h-12 w-12 text-blue-400" />
                        <div>
                          <p className="text-blue-400 font-medium">Clique para fazer upload</p>
                          <p className="text-sm text-gray-400">PNG, JPG até 10MB</p>
                        </div>
                      </div>
                    )}
                  </label>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Comparison Images Upload */}
          <Card className="border-gray-600 shadow-lg bg-gray-800/70 backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-purple-400">
                <Upload className="h-5 w-5" />
                Imagens para Comparação
              </CardTitle>
              <p className="text-sm text-gray-400">
                Selecione até 250 imagens para comparar com a imagem base
              </p>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="border-2 border-dashed border-purple-500 rounded-lg p-6 text-center hover:border-purple-400 transition-colors bg-gray-900/50">
                  <input
                    type="file"
                    ref={comparisonImagesRef}
                    onChange={handleComparisonImagesChange}
                    accept="image/*"
                    multiple
                    className="hidden"
                    id="comparison-images"
                  />
                  <label htmlFor="comparison-images" className="cursor-pointer">
                    <div className="space-y-3">
                      <Upload className="mx-auto h-12 w-12 text-purple-400" />
                      <div>
                        <p className="text-purple-400 font-medium">
                          Clique para selecionar múltiplas imagens
                        </p>
                        <p className="text-sm text-gray-400">
                          {comparisonImages.length > 0 
                            ? `${comparisonImages.length} imagem(ns) selecionada(s)`
                            : 'PNG, JPG até 10MB cada (máx. 250 imagens)'
                          }
                        </p>
                      </div>
                    </div>
                  </label>
                </div>
                
                {comparisonPreviews.length > 0 && (
                  <div className="grid grid-cols-4 gap-2 max-h-40 overflow-y-auto">
                    {comparisonPreviews.slice(0, 12).map((preview, index) => (
                      <div key={index} className="relative">
                        <img
                          src={preview.url}
                          alt={`Preview ${index + 1}`}
                          className="w-full h-16 object-cover rounded-md shadow-sm"
                        />
                      </div>
                    ))}
                    {comparisonPreviews.length > 12 && (
                      <div className="w-full h-16 bg-gray-100 rounded-md flex items-center justify-center">
                        <span className="text-xs text-gray-500">
                          +{comparisonPreviews.length - 12}
                        </span>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-wrap gap-4 justify-center mb-8">
          <Button 
            onClick={handleSubmit} 
            disabled={loading || !baseImage || comparisonImages.length === 0}
            className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-8 py-3 text-lg font-medium shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200"
          >
            {loading ? (
              <>
                <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                Processando...
              </>
            ) : (
              <>
                <CheckCircle className="mr-2 h-5 w-5" />
                Comparar Rostos
              </>
            )}
          </Button>
          
          <Button 
            onClick={resetForm} 
            variant="outline"
            className="px-8 py-3 text-lg font-medium border-2 border-gray-300 hover:border-gray-400 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200"
          >
            <RotateCcw className="mr-2 h-5 w-5" />
            Resetar
          </Button>
        </div>

        {/* Upload Progress */}
        {loading && uploadProgress > 0 && (
          <Card className="mb-8 border-gray-600 bg-gray-800/50">
            <CardContent className="pt-6">
              <div className="space-y-2">
                <div className="flex justify-between text-sm text-blue-400">
                  <span>Enviando imagens...</span>
                  <span>{uploadProgress}%</span>
                </div>
                <Progress value={uploadProgress} className="h-2" />
              </div>
            </CardContent>
          </Card>
        )}

        {/* Error Alert */}
        {error && (
          <Alert className="mb-8 border-red-500 bg-red-900/50">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription className="text-red-400">
              {error}
            </AlertDescription>
          </Alert>
        )}

        {/* Results Section */}
        {results && (
          <div className="space-y-8">
            {/* Base Image Display */}
            {results.base_image_data && (
              <Card className="border-gray-600 shadow-xl bg-gray-800/80 backdrop-blur-sm">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-blue-400 text-xl">
                    <Camera className="h-5 w-5" />
                    Imagem Base de Referência
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex justify-center">
                    <img
                      src={results.base_image_data}
                      alt="Imagem base"
                      className="max-w-xs rounded-lg shadow-lg border-2 border-blue-500"
                    />
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Results Grid */}
            <Card className="border-gray-600 shadow-xl bg-gray-800/80 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-green-400 text-2xl">
                  <CheckCircle className="h-6 w-6" />
                  Resultados da Comparação
                </CardTitle>
                <div className="flex flex-wrap gap-4 text-sm text-gray-400">
                  <span>• {results.total_images} imagens processadas</span>
                  <span>• Tempo de processamento: {results.processing_time.toFixed(2)}s</span>
                  <span>• {results.results.filter(r => r.has_face).length} rostos detectados</span>
                </div>
              </CardHeader>
              <CardContent>
                <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                  {results.results.map((result, index) => (
                    <Card key={index} className={`border-2 ${result.has_face ? 'border-green-500/50' : 'border-red-500/50'} shadow-md hover:shadow-lg transition-all duration-200 hover:-translate-y-1 bg-white/95 backdrop-blur-sm`}>
                      <CardContent className="p-6">
                        <div className="space-y-4">
                          {/* Image Display */}
                          <div className="flex justify-center">
                            {result.image_data ? (
                              <img
                                src={result.image_data}
                                alt={`Comparação ${result.image_index + 1}`}
                                className="w-32 h-32 object-cover rounded-lg shadow-md border-2 border-gray-200"
                              />
                            ) : (
                              <div className="w-32 h-32 bg-gray-100 rounded-lg flex items-center justify-center">
                                <AlertCircle className="h-8 w-8 text-gray-400" />
                              </div>
                            )}
                          </div>
                          
                          {/* Status Badge Only - Remove Image Name */}
                          <div className="flex justify-center">
                            {result.has_face ? (
                              <Badge className="bg-green-100 text-green-800 hover:bg-green-100">
                                <CheckCircle className="h-3 w-3 mr-1" />
                                Rosto Detectado
                              </Badge>
                            ) : (
                              <Badge variant="destructive" className="bg-red-100 text-red-800 hover:bg-red-100">
                                <AlertCircle className="h-3 w-3 mr-1" />
                                Sem Rosto
                              </Badge>
                            )}
                          </div>
                          
                          {/* Similarity Results */}
                          {result.has_face && !result.error_message ? (
                            <div className="space-y-3">
                              <div className="text-center">
                                <div className="text-3xl font-bold text-gray-800 mb-1">
                                  {result.similarity_percentage.toFixed(1)}%
                                </div>
                                <Badge className={`${getColorForSimilarity(result.similarity_percentage)} text-white text-sm px-3 py-1`}>
                                  Similaridade {getSimilarityLabel(result.similarity_percentage)}
                                </Badge>
                              </div>
                              <Progress 
                                value={result.similarity_percentage} 
                                className="h-3"
                              />
                            </div>
                          ) : (
                            <div className="text-center">
                              <div className="text-sm text-red-800 bg-red-100 p-3 rounded-lg">
                                {result.error_message || 'Não foi possível detectar um rosto nesta imagem'}
                              </div>
                            </div>
                          )}
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-gray-900/80 backdrop-blur-sm border-t border-gray-700 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center text-gray-400">
            <p>© 2025 Comparador Facial Painho Trampos. Tecnologia avançada de reconhecimento facial.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;