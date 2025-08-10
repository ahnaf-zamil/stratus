import type React from "react";
import { BrowserRouter, Route, Routes } from "react-router";
import { ApplicationsPage } from "./pages/Applications";
import { CreateApplicationPage } from "./pages/CreateApplication";

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/apps" element={<ApplicationsPage />} />
        <Route path="/apps/create" element={<CreateApplicationPage />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
