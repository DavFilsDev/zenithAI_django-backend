import { BrowserRouter } from 'react-router-dom';
import Header from './components/Header';

function App() {
  return (
    <BrowserRouter>
      <Header />
      {/* other routes */}
    </BrowserRouter>
  );
}

export default App
