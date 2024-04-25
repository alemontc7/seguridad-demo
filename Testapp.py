import unittest
from unittest.mock import patch
from flask import session
from bson import ObjectId
from app import app, usuarios, productos, pedidos, carrito

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_route(self):
        with self.app:
            response = self.app.get('/index')
            self.assertEqual(response.status_code, 200)

    def test_validar_cuenta_exitosa(self):
        with patch('app.session', {'usuario': 'admin', 'idUser': str(ObjectId())}):
            with patch.object(productos, 'find', return_value=[{'_id': ObjectId()}]):
                response = self.app.post('/validarCuenta', data={'Correo': 'montero.coca.alejandro@gmail.com', 'Contrasenia': 'ricolas1'})
                self.assertEqual(response.status_code, 200)

    def test_validar_cuenta_fallida(self):
        response = self.app.post('/validarCuenta', data={'Correo': 'usuario@ejemplo.com', 'Contrasenia': 'contraseña_incorrecta'})
        self.assertIn(b'El correo y/o la contrasenia son incorrectos', response.data)

    def test_agregar_producto_a_favoritos(self):
        with patch('app.session', {'usuario': 'usuario@ejemplo.com'}):
            with patch.object(usuarios, 'aggregate', return_value=[]):
                with patch.object(usuarios, 'update_one', return_value=None):
                    response = self.app.get('/agregarProductoAFavs/123456789012345678901234')
                    self.assertEqual(response.status_code, 200)

    def test_eliminar_producto_de_favoritos(self):
        with patch('app.session', {'usuario': 'usuario@ejemplo.com'}):
            with patch.object(usuarios, 'aggregate', return_value=[{'_id': ObjectId()}]):
                with patch.object(usuarios, 'update_one', return_value=None):
                    response = self.app.get('/eliminarDeFavs/123456789012345678901234')
                    self.assertEqual(response.status_code, 200)

    def test_aniadir_a_carrito(self):
        with patch('app.session', {'usuario': 'usuario@ejemplo.com', 'idUser': str(ObjectId())}):
            with patch.object(usuarios, 'find', return_value=[{'_id': ObjectId()}]):
                with patch.object(carrito, 'update_one', return_value=None):
                    response = self.app.post('/aniadirACarrito/123456789012345678901234/10.99', data={'cant': '2'})
                    self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()