use iced::{Element, Sandbox, Settings};
use iced::widget::text;
struct GroceryList {}
#[derive(Debug, Clone)]
pub enum Message {
    Increment,
    Decrement,
}
impl Sandbox for GroceryList {
	type Message = Message;
	
	/* Initialize your app */
	fn new() -> GroceryList {
		Self {}
	}
	
	/**
	* The title of the window. It will show up on the top of your application window.
	*/
	fn title(&self) -> String {
		String::from("Grocery List App")
	}
	
	fn update(&mut self, _message: Self::Message) {
		// Update the state of your app
	}
	
	fn view(&self) -> Element<Self::Message> {
		text("This is where you will show the view of your app")
		.into()
	}
}
fn main() -> iced::Result {
	GroceryList::run(Settings::default())
}