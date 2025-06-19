import "./App.css";
import RelatorioAdHoc from "./components/RelatorioAdHoc";
import { Rockets } from "./components/Rockets";
import "./components/Rockets.css";

function App() {
  return (
    <div className="app">
      <h1>SpaceX Data Explorer</h1>
      {/* <Rockets /> */}
      <RelatorioAdHoc/>
    </div>
  );
}

export default App;
