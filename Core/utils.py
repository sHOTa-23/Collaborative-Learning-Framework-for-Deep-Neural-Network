from io import BytesIO
import logging
logging.basicConfig(level=logging.NOTSET)
def prepare_model(model):
    buffer = BytesIO()
    logging.info(str(type(model).__bases__))
    model_type = str(type(model))
    model_parent_type = str(type(model).__bases__)
    if 'keras' in model_type or 'keras' in model_parent_type:
        import tensorflow as tf
        tf.get_logger().setLevel(logging.ERROR)
        from tensorflow.keras.models import save_model
        import h5py
        with h5py.File(buffer, 'w') as f:
            save_model(model, f, include_optimizer=True)
    elif 'sklearn' in model_type or 'sklearn' in model_parent_type:
        from joblib import load, dump
        dump(model, buffer)
    elif 'torch' in model_type or 'torch' in model_parent_type:
        import torch
        scripted_model = torch.jit.script(model)
        torch.jit.save(scripted_model, buffer)
    buffer.seek(0)
    return buffer.read()

def receive(client_socket, socket_buffer_size=1024):
    buffer = BytesIO()
    while True:
        data = client_socket.recv(socket_buffer_size)
        if not data:
            break
        buffer.write(data)
        buffer.seek(-4, 2)
        if b'EOF' in buffer.read():
            break
    buffer.seek(0)
    model = load_data(buffer)
    logging.info(model)
    logging.info("Received")
    return model

def load_data(file: BytesIO):
    data = file.read()[:-3]
    file.seek(0)
    if b'sklearn' in data:
        from joblib import load, dump
        return load(file)
    elif b'HDF' in data:
        import tensorflow as tf
        tf.get_logger().setLevel(logging.ERROR)
        from tensorflow.keras.models import load_model
        import h5py
        with h5py.File(file, 'r') as f:
            model = load_model(f)
            print(model.summary())
            print(print(model.trainable_variables)) 
        return model
    else:
        import torch
        model = torch.jit.load(file)
        print(model.state_dict().items())
        return model
