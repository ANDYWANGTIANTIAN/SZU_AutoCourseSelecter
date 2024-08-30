mod encryptor;

use encryptor::QuickJsEncryptor;

fn main() {
    let encryptor = QuickJsEncryptor::new();
    
    let encrypted_data = encryptor.encrypt("hello world!", "this", "password", "is");
    
    println!("Encrypted data: {}", encrypted_data);
}
