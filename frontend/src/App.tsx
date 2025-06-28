
import NavBar from "./components/NavBar";
import Footer from "./components/Footer";
import RelatorioAdHoc from "./components/RelatorioAdHoc";
import { ToastContainer } from 'react-toastify';
function App() {
  return (
    <div className="m-0 p-0 w-100">
      <NavBar/>
      <RelatorioAdHoc/>
      <ToastContainer />
      <Footer/>
    </div>
  );
}

export default App;
