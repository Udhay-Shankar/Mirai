import React, { useEffect, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { TrendingUp, Gauge, Zap, Lightbulb, ArrowRight, Check, Star } from 'lucide-react';
import MiraiLogo from './MiraiLogo';

const Landing = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const vantaRef = useRef(null);
  const vantaEffect = useRef(null);

  useEffect(() => {
    if (user) {
      navigate('/dashboard');
    }
  }, [user, navigate]);

  useEffect(() => {
    // Initialize Vanta Waves effect with delay to ensure scripts are loaded
    const initVanta = () => {
      if (!vantaEffect.current && globalThis.VANTA && globalThis.THREE) {
        try {
          vantaEffect.current = globalThis.VANTA.WAVES({
            el: vantaRef.current,
            THREE: globalThis.THREE,
            mouseControls: true,
            touchControls: true,
            gyroControls: false,
            minHeight: 200,
            minWidth: 200,
            scale: 1,
            scaleMobile: 1,
            color: 0x1a1a2e, // Dark blue-purple
            shininess: 30,
            waveHeight: 20,
            waveSpeed: 0.5,
            zoom: 0.75
          });
        } catch (error) {
          console.error('Vanta initialization error:', error);
        }
      }
    };

    // Try to initialize immediately
    initVanta();

    // If not ready, try again after a short delay
    const timer = setTimeout(initVanta, 100);
    
    return () => {
      clearTimeout(timer);
      if (vantaEffect.current) {
        vantaEffect.current.destroy();
      }
    };
  }, []);

  const features = [
    {
      icon: <Gauge className="w-7 h-7" />,
      title: 'Precision',
      description: 'Track what matters. AI filters signal from chaos with 99.2% accuracy.',
      gradient: 'from-[#1A73E8]/10 to-[#00E5FF]/10',
      accentColor: '#1A73E8'
    },
    {
      icon: <Zap className="w-7 h-7" />,
      title: 'Speed',
      description: 'Real-time alerts. Instant insights. React to trends as they happen.',
      gradient: 'from-[#00E5FF]/10 to-[#1A73E8]/10',
      accentColor: '#00E5FF'
    },
    {
      icon: <Lightbulb className="w-7 h-7" />,
      title: 'Intelligence',
      description: 'Sentiment analysis. Trend prediction. Competitor tracking powered by AI.',
      gradient: 'from-[#1A73E8]/10 to-[#00C853]/10',
      accentColor: '#00C853'
    }
  ];

  const plans = [
    {
      name: 'Starter',
      price: '0',
      tagline: 'For the curious',
      features: [
        '7-day data history',
        'Basic sentiment analysis',
        'Single keyword tracking',
        'Community support'
      ],
      accentColor: '#00E5FF'
    },
    {
      name: 'Creator',
      price: '29',
      popular: true,
      tagline: 'For the ambitious',
      features: [
        '30-day analytics',
        'Advanced AI insights',
        '10 keyword streams',
        'Priority support',
        'Export capabilities'
      ],
      accentColor: '#FF6B47'
    },
    {
      name: 'Studio',
      price: '99',
      tagline: 'For the unstoppable',
      features: [
        'Unlimited history',
        'API access',
        'Unlimited keywords',
        'White-glove support',
        'Custom workflows'
      ],
      accentColor: '#98FF98'
    }
  ];

  const stats = [
    { value: '10K+', label: 'Creators', subtext: 'trust Mirai' },
    { value: '92%', label: 'Time Saved', subtext: 'on reporting' },
    { value: '50M+', label: 'Insights', subtext: 'delivered daily' }
  ];

  return (
    <div ref={vantaRef} className="min-h-screen text-white overflow-hidden relative bg-gradient-to-br from-[#0f0c29] via-[#302b63] to-[#24243e] animate-gradient-slow">
      {/* Animated gradient fallback background */}
      <div className="absolute inset-0 opacity-80">
        <div className="absolute inset-0 bg-gradient-to-br from-[#1A73E8]/30 via-[#921102]/25 to-[#00E5FF]/30 animate-gradient-shift" />
        <div className="absolute top-0 left-0 w-full h-full">
          <div className="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-[#FF6B47]/20 rounded-full blur-3xl animate-float" />
          <div className="absolute bottom-1/4 right-1/4 w-[500px] h-[500px] bg-[#1A73E8]/20 rounded-full blur-3xl animate-float" style={{ animationDelay: '2s' }} />
          <div className="absolute top-1/2 left-1/2 w-[400px] h-[400px] bg-[#00E5FF]/15 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '4s' }} />
        </div>
      </div>
      
      {/* Content overlay with semi-transparent dark background */}
      <div className="absolute inset-0 bg-gradient-to-b from-black/60 via-black/40 to-black/60 pointer-events-none" />
      
      {/* Subtle grid overlay */}
      <div className="fixed inset-0 opacity-[0.02] pointer-events-none z-10" style={{
        backgroundImage: 'linear-gradient(white 1px, transparent 1px), linear-gradient(90deg, white 1px, transparent 1px)',
        backgroundSize: '40px 40px',
      }} />

      {/* Header - Clean & Tech */}
      <header className="fixed top-0 left-0 right-0 z-50 backdrop-blur-xl bg-black/30 border-b border-white/10">
        <div className="max-w-7xl mx-auto px-6 lg:px-12 py-5">
          <div className="flex justify-between items-center">
            {/* Logo with Mirai custom SVG */}
            <Link to="/" className="flex items-center space-x-3 relative z-20">
              <MiraiLogo size={40} />
              <span className="text-2xl font-semibold tracking-tight text-white drop-shadow-lg">Mirai</span>
            </Link>
            
            {/* Navigation */}
            <nav className="hidden md:flex items-center space-x-10 text-sm font-medium relative z-20">
              <a href="#features" className="text-white/70 hover:text-white transition-colors drop-shadow-md">Features</a>
              <a href="#pricing" className="text-white/70 hover:text-white transition-colors drop-shadow-md">Pricing</a>
              <a href="#" className="text-white/70 hover:text-white transition-colors drop-shadow-md">Customers</a>
            </nav>
            
            {/* CTA */}
            <div className="flex items-center space-x-4 relative z-20">
              <Link to="/login" className="text-sm text-white/80 hover:text-white transition-colors font-medium drop-shadow-md">
                Sign In
              </Link>
              <Link 
                to="/signup" 
                className="px-6 py-2.5 rounded-lg bg-white/90 text-black text-sm font-bold hover:bg-white hover:shadow-2xl hover:shadow-white/20 transition-all backdrop-blur-sm"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </header>

      <div className="relative z-10">
        {/* Hero Section - Clean & Impactful */}
        <section className="min-h-screen flex items-center pt-20">
          <div className="max-w-7xl mx-auto px-6 lg:px-12 py-32 w-full">
            <div className="max-w-5xl mx-auto text-center space-y-10">
              {/* Badge with enhanced visibility */}
              <div className="inline-flex items-center space-x-2 px-4 py-2 rounded-full bg-white/10 border border-white/30 backdrop-blur-md">
                <TrendingUp className="w-4 h-4 text-white" />
                <span className="text-sm text-white font-semibold drop-shadow-lg">Trusted by 10,000+ creators</span>
              </div>
              
              {/* Strategic Wrapper Headline - High contrast for Vanta background */}
              <h1 className="text-5xl md:text-7xl font-bold leading-[0.95] tracking-tight">
                <span className="text-white drop-shadow-[0_4px_30px_rgba(0,0,0,0.9)]">AWARIO DATA.</span>
                <br />
                <span className="text-white drop-shadow-[0_4px_30px_rgba(0,0,0,0.9)]">MIRAI CLARITY.</span>
                <br />
                <span className="text-white text-4xl md:text-6xl drop-shadow-[0_4px_30px_rgba(0,0,0,0.9)]">INSTANTLY.</span>
              </h1>
              
              {/* Subheadline */}
              <p className="text-lg md:text-xl text-white/90 max-w-3xl mx-auto leading-relaxed drop-shadow-lg">
                Transform your Awario data into stunning reports and actionable insights. 
                <span className="text-white font-bold"> Real-time analysis</span> that saves hours every day.
              </p>
              
              {/* CTAs with high-contrast white buttons */}
              <div className="flex flex-col sm:flex-row gap-4 justify-center pt-6">
                <Link 
                  to="/signup" 
                  className="group px-8 py-4 rounded-lg bg-white text-black font-bold hover:bg-white/90 shadow-2xl shadow-black/50 hover:shadow-white/40 transition-all hover:scale-105 flex items-center justify-center space-x-2"
                >
                  <span>Start Free Trial</span>
                  <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </Link>
                <button className="px-8 py-4 rounded-lg bg-white/10 hover:bg-white/20 border border-white/30 hover:border-white/50 backdrop-blur-md transition-all font-semibold text-white shadow-lg">
                  Watch Demo
                </button>
              </div>
              
              <p className="text-sm text-white/40 drop-shadow-md">No credit card • 14-day trial • Cancel anytime</p>
            </div>

            {/* Floating Stats Cards - High Contrast */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-32 max-w-5xl mx-auto">
              {stats.map((stat, index) => (
                <div 
                  key={index} 
                  className="group relative"
                >
                  <div className="absolute inset-0 bg-white/10 rounded-xl blur-xl opacity-50 group-hover:opacity-70 transition-all" />
                  <div className="relative p-8 rounded-xl bg-black/40 backdrop-blur-lg border border-white/20 hover:border-white/40 transition-all shadow-2xl">
                    <div className="text-5xl font-bold mb-2 text-white drop-shadow-[0_2px_20px_rgba(255,255,255,0.3)]">
                      {stat.value}
                    </div>
                    <div className="text-base text-white font-semibold drop-shadow-md">{stat.label}</div>
                    <div className="text-sm text-white/60 mt-1">{stat.subtext}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section id="features" className="py-32">
          <div className="max-w-7xl mx-auto px-6 lg:px-12">
            <div className="max-w-3xl mb-16 text-center mx-auto">
              <h2 className="text-4xl md:text-5xl font-bold mb-5 leading-tight text-white drop-shadow-[0_2px_20px_rgba(0,0,0,0.8)]">
                Built for Performance
              </h2>
              <p className="text-lg text-white/80 drop-shadow-md">
                Everything you need. <span className="text-white font-bold">Nothing you don't.</span>
              </p>
            </div>
            
            <div className="grid lg:grid-cols-3 gap-8">
              {features.map((feature, index) => (
                <div
                  key={index}
                  className="group relative"
                >
                  <div className="absolute inset-0 bg-white/5 rounded-xl blur-2xl opacity-0 group-hover:opacity-50 transition-all duration-500" />
                  <div className="relative p-10 rounded-xl bg-black/30 backdrop-blur-lg border border-white/20 hover:border-white/40 hover:bg-black/40 transition-all duration-300 h-full shadow-2xl">
                    <div 
                      className="w-14 h-14 rounded-lg flex items-center justify-center mb-6 bg-white/10 text-white shadow-lg group-hover:scale-110 group-hover:rotate-3 transition-all duration-500 border border-white/20"
                    >
                      {feature.icon}
                    </div>
                    
                    <h3 className="text-xl font-bold mb-3 text-white drop-shadow-md">{feature.title}</h3>
                    <p className="text-white/70 leading-relaxed text-sm">{feature.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Social Proof */}
        <section className="py-32">
          <div className="max-w-5xl mx-auto px-6 lg:px-12">
            <div className="relative group">
              <div className="absolute inset-0 bg-white/10 rounded-xl blur-2xl opacity-60" />
              <div className="relative p-10 md:p-12 rounded-xl bg-black/40 backdrop-blur-2xl border border-white/30 shadow-2xl">
                <div className="max-w-3xl mx-auto text-center space-y-6">
                  <div className="flex justify-center space-x-1 mb-4">
                    {[...Array(5)].map((_, i) => (
                      <Star key={i} className="w-5 h-5 text-yellow-400 fill-yellow-400 drop-shadow-lg" />
                    ))}
                  </div>
                  
                  <blockquote className="text-2xl md:text-3xl font-light leading-relaxed text-white drop-shadow-lg">
                    "Mirai cut our research from <span className="line-through text-white/40">8 hours</span> to{' '}
                    <span className="text-white font-bold">30 minutes</span>. 
                    The insights are incredibly accurate."
                  </blockquote>
                  
                  <div className="pt-3">
                    <p className="text-white font-semibold text-sm drop-shadow-md">Sarah Chen</p>
                    <p className="text-white/60 text-xs">Content Director @ TechFlow</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Pricing */}
        <section id="pricing" className="py-32">
          <div className="max-w-7xl mx-auto px-6 lg:px-12">
            <div className="max-w-3xl mb-16 text-center mx-auto">
              <h2 className="text-4xl md:text-5xl font-bold mb-5 leading-tight text-white drop-shadow-lg">
                Transparent Pricing
              </h2>
              <p className="text-lg text-white/80 drop-shadow-md">
                Start free. Scale when you're ready.
              </p>
            </div>
            
            <div className="grid lg:grid-cols-3 gap-8">
              {plans.map((plan, index) => (
                <div
                  key={index}
                  className={`relative p-10 rounded-xl backdrop-blur-xl transition-all duration-500 shadow-2xl ${
                    plan.popular
                      ? 'bg-black/50 border-2 border-white/50 scale-105 shadow-white/20'
                      : 'bg-black/30 border border-white/20 hover:border-white/40'
                  }`}
                >
                  {plan.popular && (
                    <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                      <span className="px-5 py-1.5 rounded-full bg-white text-black text-xs font-bold shadow-xl shadow-white/30 uppercase tracking-wider">
                        Most Popular
                      </span>
                    </div>
                  )}
                  
                  <div className="mb-8 pt-4">
                    <div className="text-xs text-white/70 font-bold uppercase tracking-wider mb-3">{plan.tagline}</div>
                    <h3 className="text-2xl font-bold mb-5 text-white drop-shadow-md">{plan.name}</h3>
                    <div className="flex items-baseline mb-2">
                      <span className="text-5xl font-bold text-white drop-shadow-md">${plan.price}</span>
                      <span className="text-white/50 ml-2 text-sm">/month</span>
                    </div>
                  </div>
                  
                  <ul className="space-y-3 mb-8">
                    {plan.features.map((feature, i) => (
                      <li key={i} className="flex items-start space-x-3 text-white/80 text-sm">
                        <Check className="w-4 h-4 flex-shrink-0 mt-0.5 text-white" />
                        <span className="leading-relaxed">{feature}</span>
                      </li>
                    ))}
                  </ul>
                  
                  <Link
                    to="/signup"
                    className={`block w-full text-center py-4 rounded-lg font-semibold transition-all ${
                      plan.popular
                        ? 'bg-white text-black hover:bg-white/90 hover:shadow-2xl hover:shadow-white/30 hover:scale-105'
                        : 'bg-white/10 text-white hover:bg-white/20 border border-white/30'
                    }`}
                  >
                    Get Started
                  </Link>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Final CTA */}
        <section className="py-32">
          <div className="max-w-4xl mx-auto px-6 lg:px-12">
            <div className="relative group">
              <div className="absolute inset-0 bg-white/20 rounded-xl blur-2xl opacity-40 group-hover:opacity-60 transition-all" />
              <div className="text-center p-12 rounded-xl bg-black/40 backdrop-blur-2xl border border-white/30 shadow-2xl">
                <h2 className="text-4xl md:text-5xl font-bold mb-5 text-white leading-tight drop-shadow-lg">
                  Ready to Get Started?
                </h2>
                <p className="text-lg text-white/80 mb-8 drop-shadow-md">
                  Join <span className="text-white font-bold">10,000+ creators</span> who stopped guessing and started knowing.
                </p>
                <Link 
                  to="/signup"
                  className="inline-flex items-center gap-2 px-10 py-4 bg-white text-black rounded-lg font-bold hover:bg-white/90 shadow-2xl shadow-white/30 hover:shadow-white/50 transition-all hover:scale-105 group"
                >
                  Get Started Free
                  <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </Link>
                <p className="text-xs text-white/50 mt-5">
                  No credit card required • 14-day free trial • Cancel anytime
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Footer */}
        <footer className="relative border-t border-white/10 px-6 py-12 backdrop-blur-md bg-black/30">
          <div className="max-w-7xl mx-auto">
            <div className="flex flex-col md:flex-row justify-between items-center gap-8 mb-12">
              {/* Brand */}
            <div className="flex flex-col items-center md:items-start">
              <Link to="/" className="flex items-center space-x-3 mb-4">
                <MiraiLogo size={40} />
                <span className="text-2xl font-semibold text-white drop-shadow-md">Mirai</span>
              </Link>
              <p className="text-white/50 max-w-sm text-center md:text-left">
                Social listening that actually helps you make decisions.
              </p>
            </div>              {/* Links */}
              <div className="flex gap-16">
                <div>
                  <h4 className="font-semibold mb-4 text-sm text-white">Product</h4>
                  <ul className="space-y-3 text-white/50 text-sm">
                    <li><a href="#features" className="hover:text-white transition-colors">Features</a></li>
                    <li><a href="#pricing" className="hover:text-white transition-colors">Pricing</a></li>
                    <li><a href="#" className="hover:text-white transition-colors">Changelog</a></li>
                  </ul>
                </div>
                
                <div>
                  <h4 className="font-semibold mb-4 text-sm text-white">Company</h4>
                  <ul className="space-y-3 text-white/50 text-sm">
                    <li><a href="#" className="hover:text-white transition-colors">About</a></li>
                    <li><a href="#" className="hover:text-white transition-colors">Contact</a></li>
                  </ul>
                </div>
              </div>
            </div>
            
            <div className="border-t border-white/10 pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
              <p className="text-sm text-white/40">
                © 2025 Mirai. Built for creators, by creators.
              </p>
              <div className="flex gap-6 text-sm text-white/40">
                <a href="#" className="hover:text-white transition-colors">Privacy</a>
                <a href="#" className="hover:text-white transition-colors">Terms</a>
                <a href="#" className="hover:text-white transition-colors">Security</a>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
};

export default Landing;
