---
layout:     post
title:      "Working with PaintCode and Interface Builder in XCode"
date:       2015-04-04 07:00:09
summary:    "Every self-respecting iOS developer should know about PaintCode by now, an OSX app for drawing graphics that don't save as images, but as lengths of code that draw graphics. The benefits of this are vastly reduced app installation size - no need to include three resolutions of the same image for every image - and seamlessly scalable graphics."
tags:
 - ios
 - swift
 - paintcode
 - xcode
 - xebia blog
---

*Note: This post was originally published on [the Xebia blog](http://blog.xebia.com/2015/04/04/working-with-paintcode-and-interface-builder-in-xcode/) ([archived copy](https://web.archive.org/web/20150407013333/http://blog.xebia.com/2015/04/04/working-with-paintcode-and-interface-builder-in-xcode/)) on April 4th, 2015 by me; the published date of this repost has been backdated to match. Markup has been converted from WordPress HTML to Markdown. The screenshots from the original post could not be recovered.*

---

Every self-respecting iOS developer should know about PaintCode by now, an OSX app for drawing graphics that don't save as images, but as lengths of code that draw graphics. The benefits of this are vastly reduced app installation size - no need to include three resolutions of the same image for every image - and seamlessly scalable graphics.

One thing that I personally struggled with for a while now was how to use them effectively in combination with Interface Builder, the UI development tool for iOS and OSX apps. In this blog I will explain an effective and simple method to draw PaintCode graphics in a way where you can see what you're doing in Interface Builder, using the relatively new `@IBDesignable` annotation. I will also go into setting colors, and finally about how to deal with views that depend on dynamic runtime data to draw themselves.

First, let's create a simple graphic in PaintCode. Let's draw a nice envelope or email icon. Add a frame around it, and set the constraints to variable so it will adjust to the size of the frame (drag the frame corners around within PaintCode to confirm). This gives us a nice, scalable icon. Save the file, then export it to your xcode project in the language of your choice.

*[Image no longer available: Email icon in PaintCode] (caption: "Squiggly lines are the best")*

Now, the easiest and most straightforward way to get a PaintCode image into your Interface Builder is to simply create a `UIView` subclass, and call the relevant StyleKit method in its `drawRect` method. You can do this too in either Swift or Objective-C; this example will be in Swift, but if you're stuck with the slow Swift compiler in XCode 6.x, you might prefer Objective-C for this kind of simple and straightforward code.

To use it in Interface Builder, simply create a storyboard or xib, drag an `UIView` onto it, and change its Custom Class to your `UIView` subclass. Make sure to have your constraints set properly, and run - you should be able to see your custom icon in your working app.

```swift
class EmailIcon: UIView {
  override func drawRect(rect: CGRect) {
    StyleKit.drawEmail(frame: rect)
  }
}
```

*[Image no longer available] (caption: "Ghost views, the horror of Interface Builder")*

As you probably noticed though, it's far from practical as it is in Interface Builder right now - all you see (or don't see really) is an empty `UIView`. I guess you could give it a background color in IB and unset that again in your code, but that's far from practical. Instead, we'll just slap an `@IBDesignable` annotation onto the `UIView` subclass. Going back to IB, it should start to compile code, and a moment later, your PaintCode image shows up, resizable and all.

```swift
@IBDesignable
class EmailIcon: UIView {
  override func drawRect(rect: CGRect) {
    StyleKit.drawEmail(frame: rect)
  }
}
```

*[Image no longer available: @IBDesignable view in Interface Builder] (caption: "like magic")*

## Adding color

We can configure our graphic in PaintCode to have a custom color. Just go back to PaintCode and change the Color to 'Parameter' - see image.

*[Image no longer available: Set color to Parameter]*

Export the file again, and change the call to the StyleKit method to include the color. It's easiest in this case to just pass the `UIView`'s own `tintColor` property. Going back to Interface Builder, we can now set the default `tintColor` property, and it should update in the IB preview instantly.

As an alternative, you can add an [`@IBInspectable`](https://developer.apple.com/library/ios/recipes/xcode_help-IB_objects_media/Chapters/CreatingaLiveViewofaCustomObject.html) color property to your `UIView`, but I would only recommend this for more complicated `UIView`s - if they include multiple StyleKit graphics, for example.

```swift
@IBDesignable
class EmailIcon: UIView {
  override func drawRect(rect: CGRect) {
    StyleKit.drawEmail(frame: rect, color: tintColor)
  }
}
```

*[Image no longer available] (caption: "let's make it Xebia purple, to please the boss")*

## Dealing with dynamic properties

One case I had to deal with is an UIView that can draw a selection of StyleKit images, depending on the value of a dynamic model value. I considered a few options to deal with that:

1. Set a default value, to be overridden at runtime. This is a bit dangerous though; forget to reset or unset this property at runtime and your user will be stuck with some default placeholder, or worse, flat-out wrong information.
2. Make the property `@IBInspectable`. This only works with relatively simple values though (strings, numbers, colors), and it has the same problem as the above.

What I needed was a way to set a property, but only from within Interface Builder. Luckily, that exists, as I found out later. In UIView, there is a method called prepareForInterfaceBuilder, which does exactly what it says on the tin - override the method to set properties only relevant in Interface Builder. So in our case:

```swift
@IBDesignable
class EmailIcon: UIView {
  // none set by default
  var iconType: String? = nil

  override func drawRect(rect: CGRect) {
    if iconType == "email" {
      StyleKit.drawEmail(frame: rect, color: tintColor)
    }

    if iconType = "email-read" {
      StyleKit.drawEmailRead(frame: rect, color: tintColor)
    }

    // if none of the above, draw nothing
  }

  // draw the 'email' icon by default in Interface Builder
  override func prepareForInterfaceBuilder() {
    iconType = "email"
  }
}
```

And that's all there is to it. You can use this method to create all of your graphics, keep them dynamically sized and colored, and to use the full power of Interface Builder and PaintCode combined.
