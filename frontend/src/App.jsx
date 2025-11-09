import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingLenis from './components/LandingLenis';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingLenis />} />
      </Routes>
    </Router>
  );
}

export default App;
