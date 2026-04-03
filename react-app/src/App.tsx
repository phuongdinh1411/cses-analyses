import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import HomePage from './pages/HomePage'
import ContentPage from './pages/ContentPage'
import ByteByteGoIndex from './pages/ByteByteGoIndex'
import ByteBytegoCourseIndex from './pages/ByteBytegoCourseIndex'

function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/bytebytego" element={<ByteByteGoIndex />} />
        <Route path="/bytebytego/:courseKey" element={<ByteBytegoCourseIndex />} />
        <Route path="*" element={<ContentPage />} />
      </Route>
    </Routes>
  )
}

export default App
