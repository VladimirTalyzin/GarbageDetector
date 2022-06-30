document.addEventListener("DOMContentLoaded", () =>
{
	const webCameraPlace = document.getElementById("web-camera")

	const screenWidth = window.innerWidth
	const screeHeight = window.innerHeight
	let width
	let height

	if (screenWidth > screeHeight)
	{
		width = Math.round(4 / 3 * screeHeight / 2)
		height = Math.round(screeHeight / 2)
	}
	else
	{
		width = screenWidth
		height = Math.round(screenWidth * 3 / 4)
	}

	webCameraPlace.style.width = width + "px"
	webCameraPlace.style.height = height + "px"

	const webCamera = new WebCamera(webCameraPlace, "environment", width, height)

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

	const header = document.getElementById("header")
	const getPhoto = document.getElementById("get-photo")
	getPhoto.addEventListener("click", () =>
	{
		const postData = new FormData()
		postData.append("photo", webCamera.getPhoto())
		const saveText = getPhoto.innerHTML
		getPhoto.innerHTML = "⟳"
		getPhoto.style.pointerEvents = "none"

		fetch("https://0v.ru/garbage/detect.php", {method: "POST", body: postData}).then(response =>
		{
			getPhoto.innerHTML = saveText
			getPhoto.style.pointerEvents = null

			if (response.ok)
			{
				response.text().then((text) =>
				{
					const answer = JSON.parse(text)
					if (answer.hasOwnProperty("error"))
					{
						alert(answer["error"])
					}
					else if (answer.hasOwnProperty("class"))
					{
						switch (answer["class"])
						{
							case 0:
							{
								header.innerHTML = "Помойка не обнаружена"
								break
							}

							case 1:
							{
								header.innerHTML = "Помойка найдена"
								break
							}

							case 2:
							{
								header.innerHTML = "Плохое качество"
								break
							}
						}
					}
					else
					{
						alert("Распознавание не удалось")
					}
				})
			}
			else
			{
				throw new Error('Error')
			}
		})
		.catch(error => console.log(error))
	})
})