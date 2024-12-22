import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import Search from './components/Search';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import IndividualInfo from './components/IndividualInfo';
import BackgroundCircles from './components/Circles';

function App() {
  BackgroundCircles();
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Search />} />
        <Route path='/:locale/class/:nameClass/individual/:individualIri' element={<IndividualInfo />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
