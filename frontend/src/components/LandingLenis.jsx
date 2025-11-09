import React, { useEffect, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import MiraiLogo from './MiraiLogo';
import { SpotlightCard } from './ui/spotlight-card';
import ShinyCard from './ui/shiny-card';

const LandingLenis = () => {
  const navigate = useNavigate();
  const lenisRef = useRef(null);
  const scrollRef = useRef(0);

  useEffect(() => {
    let vantaEffect = null;

    // Initialize Vanta.js Waves
    const initVanta = () => {
      const vantaEl = document.getElementById('vanta-bg');
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

    // Wait for Vanta to load
    const checkVanta = setInterval(() => {
      if (window.VANTA && window.THREE) {
        clearInterval(checkVanta);
        initVanta();
      }
    }, 100);

    // Initialize Lenis smooth scroll
    const initLenis = async () => {
      if (typeof window !== 'undefined') {
        const Lenis = (await import('lenis')).default;
        
        lenisRef.current = new Lenis({
          duration: 1.2,
          easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
          orientation: 'vertical',
          gestureOrientation: 'vertical',
          smoothWheel: true,
          wheelMultiplier: 1,
          smoothTouch: false,
          touchMultiplier: 2,
          infinite: false,
        });

        function raf(time) {
          lenisRef.current?.raf(time);
          requestAnimationFrame(raf);
        }

        requestAnimationFrame(raf);

        // Parallax effect on scroll
        lenisRef.current.on('scroll', ({ scroll }) => {
          scrollRef.current = scroll;
          
          // Update background position for parallax
          const parallaxElements = document.querySelectorAll('[data-parallax]');
          parallaxElements.forEach((el) => {
            const speed = parseFloat(el.getAttribute('data-speed')) || 0.5;
            el.style.transform = `translate3d(0, ${scroll * speed}px, 0)`;
          });
        });
      }
    };

    initLenis();

    // Intersection Observer for scroll animations
    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animate-in');
        }
      });
    }, observerOptions);

    // Observe all elements with data-animate attribute
    setTimeout(() => {
      const animateElements = document.querySelectorAll('[data-animate]');
      animateElements.forEach(el => observer.observe(el));
    }, 100);

    return () => {
      lenisRef.current?.destroy();
      observer.disconnect();
      if (vantaEffect) vantaEffect.destroy();
      clearInterval(checkVanta);
    };
  }, []);

  return (
    <div className="bg-[#0a0a0a] text-white font-sans relative overflow-hidden">
      {/* Vanta.js Waves Background */}
      <div 
        id="vanta-bg" 
        className="fixed inset-0 pointer-events-none"
        style={{ zIndex: 0 }}
      />
      
      {/* Animated gradient overlay for extra depth */}
      <div className="fixed inset-0 opacity-20 pointer-events-none" style={{ zIndex: 1 }}>
        <div 
          className="absolute inset-0 bg-gradient-to-br from-purple-600/30 via-transparent to-cyan-600/30"
          style={{
            animation: 'gradientShift 20s ease infinite',
            backgroundSize: '400% 400%'
          }}
        />
      </div>

      {/* Floating halos with parallax */}
      <div className="fixed inset-0 pointer-events-none" style={{ zIndex: 1 }}>
        <div 
          className="absolute top-[10%] right-[10%] w-[600px] h-[600px] bg-blue-500/20 rounded-full blur-[100px]"
          data-parallax
          data-speed="0.3"
          style={{ animation: 'pulse 8s ease-in-out infinite' }}
        />
        <div 
          className="absolute bottom-[20%] left-[5%] w-[500px] h-[500px] bg-purple-500/20 rounded-full blur-[100px]"
          data-parallax
          data-speed="0.5"
          style={{ animation: 'pulse 10s ease-in-out infinite 2s' }}
        />
        <div 
          className="absolute top-[40%] left-[50%] w-[700px] h-[700px] bg-cyan-500/15 rounded-full blur-[120px] -translate-x-1/2"
          data-parallax
          data-speed="0.4"
          style={{ animation: 'pulse 12s ease-in-out infinite 4s' }}
        />
      </div>

      {/* Minimal Header */}
      <header className="fixed top-0 left-0 right-0 border-b border-white/5 bg-[#0a0a0a]/80 backdrop-blur-2xl" style={{ zIndex: 50 }}>
        <div className="max-w-[1600px] mx-auto px-8 lg:px-16 py-6 flex justify-between items-center">
          <Link to="/" className="flex items-center space-x-3 group">
            <div className="transition-transform group-hover:scale-110 duration-300">
              <MiraiLogo size={32} />
            </div>
            <span className="text-xl font-bold tracking-tight font-mirai">MIRAI</span>
          </Link>
          
          <nav className="hidden md:flex items-center space-x-10 text-sm">
            <a href="#features" className="text-white/50 hover:text-white transition-all duration-300">Features</a>
            <a href="#pricing" className="text-white/50 hover:text-white transition-all duration-300">Pricing</a>
            <a href="#about" className="text-white/50 hover:text-white transition-all duration-300">About</a>
          </nav>
          
          <div className="flex items-center gap-6">
            <Link to="/login" className="text-sm text-white/50 hover:text-white transition-all duration-300">
              Sign In
            </Link>
            <Link 
              to="/signup" 
              className="px-6 py-2.5 bg-white text-black text-sm font-medium hover:bg-white/90 transition-all duration-300 hover:scale-105"
            >
              Sign Up
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section - Full viewport with parallax */}
      <section className="min-h-screen flex items-center justify-center px-8 pt-32 pb-24 relative" style={{ zIndex: 10 }}>
        <div className="max-w-[1600px] w-full relative">
          <div className="grid lg:grid-cols-2 gap-20 items-center">
            {/* Left: Main Message */}
            <div className="space-y-10" data-parallax data-speed="0.1">
              <div className="space-y-6">
                <h1 className="text-7xl lg:text-8xl font-bold leading-[0.85] tracking-tighter">
                  <span className="block" style={{ animation: 'fadeSlideUp 0.6s ease-out 0.1s backwards' }}>
                    SOCIAL
                  </span>
                  <span className="block" style={{ animation: 'fadeSlideUp 0.6s ease-out 0.2s backwards' }}>
                    INSIGHTS.
                  </span>
                  <span className="block text-white/30" style={{ animation: 'fadeSlideUp 0.6s ease-out 0.3s backwards' }}>
                    INSTANTLY.
                  </span>
                </h1>
              </div>
              
              <p className="text-xl text-white/60 max-w-xl leading-relaxed" style={{ animation: 'fadeSlideUp 0.6s ease-out 0.4s backwards' }}>
                Track brand mentions, analyze sentiment, and discover trends across all social media platforms—all in one powerful dashboard.
                <span className="block mt-3 text-white/40">Real-time monitoring · AI-powered analysis · Actionable insights</span>
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 pt-6" style={{ animation: 'fadeSlideUp 0.6s ease-out 0.5s backwards' }}>
                <Link 
                  to="/signup" 
                  className="group inline-flex items-center justify-center gap-3 px-10 py-5 bg-white text-black font-medium hover:bg-white/90 transition-all duration-300 hover:scale-105"
                >
                  <span>Start Tracking Social Media</span>
                  <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform duration-300" />
                </Link>
                <button className="inline-flex items-center justify-center px-10 py-5 border border-white/10 hover:border-white/20 hover:bg-white/5 transition-all duration-300">
                  See Analytics Demo
                </button>
              </div>
              
              <div className="flex items-center gap-8 pt-4 text-sm text-white/50" style={{ animation: 'fadeSlideUp 0.6s ease-out 0.6s backwards' }}>
                <div className="flex items-center gap-2">
                  <svg className="w-5 h-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/>
                  </svg>
                  <span>No credit card required</span>
                </div>
                <div className="flex items-center gap-2">
                  <svg className="w-5 h-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/>
                  </svg>
                  <span>All platforms included</span>
                </div>
              </div>
              
            </div>

            {/* Right: Floating Stats */}
            <div className="relative h-[600px]" data-parallax data-speed="0.2">
              <div className="absolute inset-0">
                {[
                  { label: 'SOCIAL PROFILES', value: '10K+', x: '0%', y: '0%', delay: '0s', desc: 'Tracked' },
                  { label: 'MENTIONS/DAY', value: '50M+', x: '50%', y: '10%', delay: '0.1s', desc: 'Analyzed' },
                  { label: 'SENTIMENT ACCURACY', value: '92%', x: '10%', y: '40%', delay: '0.2s', desc: 'AI-Powered' },
                  { label: 'UPTIME', value: '99.9%', x: '55%', y: '50%', delay: '0.3s', desc: 'Reliable' },
                ].map((stat, idx) => (
                  <div 
                    key={idx} 
                    className="absolute border border-white/10 bg-[#0a0a0a]/60 backdrop-blur-xl p-8 hover:border-white/20 hover:bg-[#0a0a0a]/80 transition-all duration-500 hover:scale-105"
                    style={{
                      left: stat.x,
                      top: stat.y,
                      animation: `floatIn 1s ease-out ${stat.delay} backwards`
                    }}
                  >
                    <div className="text-xs text-white/30 tracking-wider mb-3">{stat.label}</div>
                    <div className="text-5xl font-bold mb-2">{stat.value}</div>
                    <div className="text-xs text-white/40 mb-3">{stat.desc}</div>
                    <div className="w-16 h-[2px] bg-gradient-to-r from-white/20 to-transparent" />
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section - Minimal Grid */}
      <section id="features" className="py-40 px-8 border-t border-white/5 relative" style={{ zIndex: 10 }}>
        <div className="max-w-[1600px] mx-auto">
          <div className="mb-24 opacity-0 translate-y-10 transition-all duration-1000" data-animate data-parallax data-speed="0.15">
            <div className="text-sm text-white/30 tracking-[0.2em] uppercase mb-6">
              Social Media Analytics Features
            </div>
            <h2 className="text-6xl lg:text-7xl font-bold leading-tight max-w-3xl">
              Everything You Need to Monitor Social Media
            </h2>
            <p className="text-xl text-white/40 mt-6 max-w-2xl">
              From tracking brand mentions to analyzing audience sentiment—get complete visibility across all platforms.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              { num: '01', title: 'Social Listening', desc: 'Monitor brand mentions across platforms. Track conversations in real-time with Awario integration.', color: 'blue' },
              { num: '02', title: 'Sentiment Analysis', desc: 'AI-powered emotion detection. Understand audience reactions with positive, neutral, negative insights.', color: 'purple' },
              { num: '03', title: 'Trend Detection', desc: 'Identify viral content patterns. Spot emerging trends before competitors with smart alerts.', color: 'cyan' },
              { num: '04', title: 'Influencer Discovery', desc: 'Find key voices in your niche. Analyze reach, engagement, and influence metrics automatically.', color: 'green' },
              { num: '05', title: 'Visual Reports', desc: 'Beautiful charts and word clouds. Export data as CSV, JSON, or visual presentations.', color: 'orange' },
              { num: '06', title: 'Creator Dashboard', desc: 'Unified analytics hub. Track mentions, sentiment, and trending topics in one place.', color: 'red' },
            ].map((feature, idx) => (
              <div 
                key={idx}
                className="opacity-0 translate-y-10"
                data-animate
                style={{ transitionDelay: `${idx * 100}ms` }}
              >
                <SpotlightCard
                  glowColor={feature.color}
                  customSize={true}
                  width="100%"
                  height="280px"
                  className="h-full"
                >
                  <div className="flex flex-col h-full justify-between">
                    <div className="space-y-5">
                      <div className="text-sm text-white/20">{feature.num}</div>
                      <h3 className="text-2xl font-bold">{feature.title}</h3>
                      <p className="text-sm text-white/40 leading-relaxed">{feature.desc}</p>
                    </div>
                    <div className="w-12 h-[2px] bg-gradient-to-r from-white/10 to-transparent" />
                  </div>
                </SpotlightCard>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Section - Clean Table */}
      <section id="pricing" className="py-40 px-8 border-t border-white/5 relative" style={{ zIndex: 10 }}>
        <div className="max-w-[1600px] mx-auto">
          <div className="mb-24 opacity-0 translate-y-10 transition-all duration-1000" data-animate data-parallax data-speed="0.15">
            <div className="text-sm text-white/30 tracking-[0.2em] uppercase mb-6">
              Pricing
            </div>
            <h2 className="text-6xl lg:text-7xl font-bold leading-tight">
              Transparent.<br />No Surprises.
            </h2>
          </div>

          <div className="grid lg:grid-cols-3 gap-8">
            {[
              { name: 'STARTER', price: '0', period: 'FREE', features: ['7-day history', 'Basic analytics', '1 keyword', 'Community support'], popular: false },
              { name: 'PRO', price: '29', period: 'PER MONTH', features: ['90-day history', 'Advanced analytics', 'Unlimited keywords', 'Priority support'], popular: true },
              { name: 'ENTERPRISE', price: '99', period: 'PER MONTH', features: ['Unlimited history', 'API access', 'Custom workflows', 'White-glove support'], popular: false },
            ].map((plan, idx) => (
              <div 
                key={idx}
                className="opacity-0 translate-y-10"
                data-animate
                style={{ transitionDelay: `${idx * 150}ms` }}
              >
                <ShinyCard
                  featureName={plan.name}
                  price={plan.price}
                  period={plan.period}
                  featureItems={plan.features}
                  popular={plan.popular}
                  className={plan.popular ? 'lg:scale-105' : ''}
                />
                
                <Link
                  to="/signup"
                  className={`block w-full text-center py-5 font-medium transition-all duration-300 hover:scale-105 mt-6 ${
                    plan.popular
                      ? 'bg-white text-black hover:bg-white/90'
                      : 'border border-white/10 hover:border-white/20 hover:bg-white/5 text-white'
                  }`}
                >
                  Get Started
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section with gradient */}
      <section className="py-40 px-8 border-t border-white/5 relative overflow-hidden" style={{ zIndex: 10 }}>
        <div 
          className="absolute inset-0 bg-gradient-to-br from-purple-600/5 via-transparent to-blue-600/5"
          data-parallax
          data-speed="0.3"
        />
        <div className="max-w-[1200px] mx-auto text-center space-y-12 relative">
          <h2 className="text-6xl lg:text-8xl font-bold leading-tight">
            Stop Guessing.<br />
            <span className="text-white/30">Start Knowing.</span>
          </h2>
          <p className="text-2xl text-white/50 max-w-2xl mx-auto">
            Join 10,000+ creators using Mirai for data-driven decisions.
          </p>
          <Link 
            to="/signup"
            className="inline-flex items-center gap-4 px-12 py-6 bg-white text-black text-lg font-medium hover:bg-white/90 transition-all duration-300 hover:scale-105"
          >
            Start Free Trial
            <ArrowRight className="w-6 h-6" />
          </Link>
        </div>
      </section>

      {/* Footer - Ultra Minimal */}
      <footer className="border-t border-white/5 px-8 py-16 bg-[#0a0a0a]/80 backdrop-blur-2xl relative" style={{ zIndex: 10 }}>
        <div className="max-w-[1600px] mx-auto">
          <div className="flex flex-col md:flex-row justify-between gap-12 mb-16">
            <div className="space-y-6">
              <div className="flex items-center space-x-3">
                <MiraiLogo size={28} />
                <span className="text-lg font-bold font-mirai">MIRAI</span>
              </div>
              <p className="text-sm text-white/30 max-w-sm">
                Social listening that helps you make data-driven decisions.
              </p>
            </div>
            
            <div className="grid grid-cols-2 md:grid-cols-3 gap-16 text-sm">
              <div className="space-y-4">
                <div className="text-white/20 text-xs tracking-wider">PRODUCT</div>
                <ul className="space-y-3">
                  <li><a href="#features" className="text-white/40 hover:text-white transition-colors duration-300">Features</a></li>
                  <li><a href="#pricing" className="text-white/40 hover:text-white transition-colors duration-300">Pricing</a></li>
                  <li><a href="#changelog" className="text-white/40 hover:text-white transition-colors duration-300">Changelog</a></li>
                </ul>
              </div>
              
              <div className="space-y-4">
                <div className="text-white/20 text-xs tracking-wider">COMPANY</div>
                <ul className="space-y-3">
                  <li><a href="#about" className="text-white/40 hover:text-white transition-colors duration-300">About</a></li>
                  <li><a href="#blog" className="text-white/40 hover:text-white transition-colors duration-300">Blog</a></li>
                  <li><a href="#contact" className="text-white/40 hover:text-white transition-colors duration-300">Contact</a></li>
                </ul>
              </div>
              
              <div className="space-y-4">
                <div className="text-white/20 text-xs tracking-wider">LEGAL</div>
                <ul className="space-y-3">
                  <li><a href="#privacy" className="text-white/40 hover:text-white transition-colors duration-300">Privacy</a></li>
                  <li><a href="#terms" className="text-white/40 hover:text-white transition-colors duration-300">Terms</a></li>
                  <li><a href="#security" className="text-white/40 hover:text-white transition-colors duration-300">Security</a></li>
                </ul>
              </div>
            </div>
          </div>
          
          <div className="pt-8 border-t border-white/5 flex flex-col md:flex-row justify-between items-center gap-4 text-xs text-white/20">
            <p>© 2025 Mirai. Built for creators, by creators.</p>
            <p>Smooth scroll powered by Lenis</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingLenis;
