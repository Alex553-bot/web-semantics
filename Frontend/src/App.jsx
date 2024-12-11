import 'bootstrap/dist/css/bootstrap.min.css';
import Search from './components/Search';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import IndividualInfo from './components/IndividualInfo';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Search />} />
        <Route path='/class/:nameClass/individual/:individualName' element={<IndividualInfo />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
