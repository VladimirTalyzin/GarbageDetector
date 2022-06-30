document.addEventListener("DOMContentLoaded", () =>
{
	const webCameraPlace = document.getElementById("web-camera")
	const webCamera = new WebCamera(webCameraPlace, "environment")

	webCamera.flip()

	webCamera.start().then(() =>
	{
		console.log("Camera started")
	})
	.catch((exception) =>
	{
		console.log(exception)
	})

	document.getElementById("switch-face").addEventListener("click", () =>
	{
		webCamera.flip()
	})

	let mirror = true
	document.getElementById("mirror").addEventListener("click", () =>
	{
		mirror = !mirror
		if (mirror)
		{
			webCameraPlace.style.transform = "scaleX(-1)"
		}
		else
		{
			webCameraPlace.style.transform = null
		}
	})

	document.getElementById("get-photo").addEventListener("click", () =>
	{
		const image = webCamera.getPhoto()
	})
})