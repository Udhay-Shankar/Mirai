import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Mail, Lock, Eye, EyeOff } from 'lucide-react';
import MiraiLogo from './MiraiLogo';
import { SocialButton } from './base/buttons/social-button';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { signInWithEmail, signInWithGoogle, signInWithFacebook, signInWithApple, signInWithTwitter } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    // Initialize Vanta.js Waves
    let vantaEffect = null;
    
    const initVanta = () => {
      const vantaEl = document.getElementById('vanta-bg-login');
      if (vantaEl && window.VANTA && window.THREE) {
        vantaEffect = window.VANTA.WAVES({
          el: vantaEl,
          THREE: window.THREE,
          mouseControls: true,
          touchControls: true,
          gyroControls: false,
          minHeight: 200.00,
          minWidth: 200.00,
          scale: 1.00,
          scaleMobile: 1.00,
          color: 0x0a0a0a,
          shininess: 40.00,
          waveHeight: 15.00,
          waveSpeed: 0.75,
          zoom: 0.85
        });
      }
    };

    const checkVanta = setInterval(() => {
      if (window.VANTA && window.THREE) {
        clearInterval(checkVanta);
        initVanta();
      }
    }, 100);

    return () => {
      if (vantaEffect) vantaEffect.destroy();
      clearInterval(checkVanta);
    };
  }, []);

  const handleEmailLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await signInWithEmail(email, password);
      navigate('/dashboard');
    } catch (err) {
      setError('Failed to log in. Please check your credentials.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleLogin = async () => {
    setError('');
    setLoading(true);

    try {
      await signInWithGoogle();
      navigate('/dashboard');
    } catch (err) {
      setError('Failed to log in with Google.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleFacebookLogin = async () => {
    setError('');
    setLoading(true);

    try {
      await signInWithFacebook();
      navigate('/dashboard');
    } catch (err) {
      setError('Failed to log in with Facebook.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAppleLogin = async () => {
    setError('');
    setLoading(true);

    try {
      await signInWithApple();
      navigate('/dashboard');
    } catch (err) {
      setError('Failed to log in with Apple.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleTwitterLogin = async () => {
    setError('');
    setLoading(true);

    try {
      await signInWithTwitter();
      navigate('/dashboard');
    } catch (err) {
      setError('Failed to log in with X.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0a0a0a] flex items-center justify-center p-4 relative overflow-hidden">
      {/* SVG Filter for liquid glass effect */}
      <svg width="0" height="0" style={{ position: 'absolute' }}>
        <defs>
          <filter id="glass-distortion" x="0%" y="0%" width="100%" height="100%">
            <feTurbulence 
              type="fractalNoise" 
              baseFrequency="0.008 0.008"
              numOctaves="2" 
              seed="92" 
              result="noise" 
            />
            <feGaussianBlur 
              in="noise" 
              stdDeviation="2" 
              result="blurred" 
            />
            <feDisplacementMap 
              in="SourceGraphic" 
              in2="blurred" 
              scale="150"
              xChannelSelector="R" 
              yChannelSelector="G" 
            />
          </filter>
        </defs>
      </svg>

      {/* Vanta.js Waves Background */}
      <div 
        id="vanta-bg-login" 
        className="fixed inset-0"
        style={{ zIndex: 0 }}
      />
      
      {/* Animated gradient overlay - matching background colors */}
      <div className="fixed inset-0 opacity-15 pointer-events-none" style={{ zIndex: 1 }}>
        <div 
          className="absolute inset-0 bg-gradient-to-br from-blue-900/40 via-purple-900/30 to-cyan-900/40"
          style={{
            animation: 'gradientShift 20s ease infinite',
            backgroundSize: '400% 400%'
          }}
        />
      </div>

      {/* Floating halos - darker to match background */}
      <div className="fixed inset-0 pointer-events-none" style={{ zIndex: 1 }}>
        <div 
          className="absolute top-1/4 right-1/4 w-[500px] h-[500px] bg-blue-900/30 rounded-full blur-[120px]"
          style={{ animation: 'pulse 8s ease-in-out infinite' }}
        />
        <div 
          className="absolute bottom-1/3 left-1/3 w-[400px] h-[400px] bg-purple-900/25 rounded-full blur-[100px]"
          style={{ animation: 'pulse 10s ease-in-out infinite 2s' }}
        />
      </div>
      
      <div className="max-w-md w-full relative" style={{ zIndex: 10 }}>
        {/* Logo */}
        <div className="text-center mb-8">
          <Link to="/" className="inline-flex items-center space-x-3 justify-center group">
            <div className={`transition-transform ${loading ? 'animate-spin' : 'group-hover:scale-110'} duration-300`}>
              <MiraiLogo size={48} />
            </div>
            <span className="text-4xl font-bold text-white font-mirai">Mirai</span>
          </Link>
          <p className="text-white/60 mt-3 text-lg">Welcome back!</p>
        </div>

        {/* Liquid Glass Card */}
        <div className="liquid-glass-card relative" style={{ 
          width: '100%', 
          height: 'auto',
          minHeight: '500px',
          borderRadius: '28px',
          boxShadow: '0px 6px 21px -8px rgba(255, 255, 255, 0.2)',
        }}>
          {/* Tint and inner shadow layer */}
          <div style={{
            position: 'absolute',
            inset: 0,
            zIndex: 0,
            borderRadius: '28px',
            boxShadow: 'inset 0 0 12px -4px rgba(255, 255, 255, 0.3)',
            backgroundColor: 'rgba(10, 10, 10, 0.3)',
            pointerEvents: 'none'
          }} />

          {/* Backdrop blur and distortion layer */}
          <div style={{
            position: 'absolute',
            inset: 0,
            zIndex: -1,
            borderRadius: '28px',
            backdropFilter: 'blur(20px)',
            WebkitBackdropFilter: 'blur(20px)',
            filter: 'url(#glass-distortion)',
            WebkitFilter: 'url(#glass-distortion)',
            isolation: 'isolate',
            pointerEvents: 'none',
            backgroundColor: 'rgba(10, 10, 10, 0.4)'
          }} />

          {/* Content */}
          <div className="relative z-10 p-8">
            <h2 className="text-2xl font-bold mb-6 text-center text-white">Log In</h2>

            {error && (
              <div className="bg-red-500/10 border border-red-500/50 text-red-400 px-4 py-3 rounded-lg mb-6 text-sm backdrop-blur-sm">
                {error}
              </div>
            )}

            {/* Social Login Buttons */}
            <div className="grid grid-cols-3 gap-3 mb-6">
              <SocialButton 
                social="google" 
                theme="brand"
                onClick={handleGoogleLogin}
                disabled={loading}
              />
              <SocialButton 
                social="facebook" 
                theme="brand"
                onClick={handleFacebookLogin}
                disabled={loading}
              />
              <SocialButton 
                social="twitter" 
                theme="brand"
                onClick={handleTwitterLogin}
                disabled={loading}
              />
            </div>

            <div className="relative mb-6">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-white/10"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-3 bg-[#0a0a0a]/50 text-white/40 backdrop-blur-sm">Or continue with email</span>
              </div>
            </div>

            {/* Email Login Form */}
            <form onSubmit={handleEmailLogin} className="space-y-5">
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-white/70 mb-2">
                  Email
                </label>
                <div className="relative">
                  <Mail className="absolute left-4 top-3.5 w-5 h-5 text-white/40" />
                  <input
                    id="email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    className="w-full pl-12 pr-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:border-white/30 focus:outline-none transition-colors text-white placeholder-white/30 backdrop-blur-sm"
                    placeholder="you@example.com"
                  />
                </div>
              </div>

              <div>
                <label htmlFor="password" className="block text-sm font-medium text-white/70 mb-2">
                  Password
                </label>
                <div className="relative">
                  <Lock className="absolute left-4 top-3.5 w-5 h-5 text-white/40" />
                  <input
                    id="password"
                    type={showPassword ? "text" : "password"}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    className="w-full pl-12 pr-12 py-3 bg-white/5 border border-white/10 rounded-lg focus:border-white/30 focus:outline-none transition-colors text-white placeholder-white/30 backdrop-blur-sm"
                    placeholder="••••••••"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-4 top-3.5 text-white/40 hover:text-white/70 transition-colors"
                  >
                    {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-3 bg-white text-black font-medium rounded-lg hover:bg-white/90 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl"
              >
                {loading ? 'Logging in...' : 'Log In'}
              </button>
            </form>

            <p className="text-center text-white/50 mt-6">
              Don't have an account?{' '}
              <Link to="/signup" className="text-white font-medium hover:underline">
                Sign up
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
