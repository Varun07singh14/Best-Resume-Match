import Feed from "./components/Feed";
import Home from "./components/Home";
import { BrowserRouter, Routes, Route } from "react-router-dom";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />}></Route>
        <Route path="/jobs" element={<Feed category="job" />}></Route>
        <Route path="/resumes" element={<Feed category="resume" />}></Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
