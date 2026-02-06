import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Shell from './components/layout/Shell'
import Home from './pages/Home'
import Decision from './pages/Decision'
import Study from './pages/Study'
import Hygiene from './pages/Hygiene'
import Food from './pages/Food'
import Sleep from './pages/Sleep'
import Fitness from './pages/Fitness'
import Songs from './pages/Songs'
import Movies from './pages/Movies'
import Football from './pages/Football'

export default function App() {
  return (
    <BrowserRouter>
      <Shell>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/decision" element={<Decision />} />
          <Route path="/study" element={<Study />} />
          <Route path="/hygiene" element={<Hygiene />} />
          <Route path="/food" element={<Food />} />
          <Route path="/sleep" element={<Sleep />} />
          <Route path="/fitness" element={<Fitness />} />
          <Route path="/songs" element={<Songs />} />
          <Route path="/movies" element={<Movies />} />
          <Route path="/football" element={<Football />} />
        </Routes>
      </Shell>
    </BrowserRouter>
  )
}
