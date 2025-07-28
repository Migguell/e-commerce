import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { CartProvider } from './context/CartContext';
import { ProductProvider } from './context/ProductContext';
import { AppProvider } from './context/AppContext';
import Header from './components/Header/Header';
import HomePage from './components/HomePage/HomePage';
import ProductGrid from './components/ProductGrid/ProductGrid';
import ProductDetail from './components/ProductDetail/ProductDetail';
import Cart from './components/Cart/Cart';
import Login from './components/Login/Login';
import Register from './components/Register/Register';
import Profile from './components/Profile/Profile';
import './App.css';

function App() {
  return (
    <AppProvider>
      <ProductProvider>
        <CartProvider>
          <Router>
            <div className="App">
              <Header />
              <main className="main-content">
                <Routes>
                  <Route path="/" element={<HomePage />} />
                  <Route path="/products" element={<ProductGrid />} />
                  <Route path="/products/:id" element={<ProductDetail />} />
                  <Route path="/cart" element={<Cart />} />
                  <Route path="/login" element={<Login />} />
                  <Route path="/register" element={<Register />} />
                  <Route path="/profile" element={<Profile />} />
                </Routes>
              </main>
            </div>
          </Router>
        </CartProvider>
      </ProductProvider>
    </AppProvider>
  );
}

export default App;
