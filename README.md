<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
<!--
[![LinkedIn][linkedin-shield]][linkedin-url]
-->



<!-- PROJECT LOGO -->
<br />
<!--
<div align="center">
  <a href="https://github.com/BetterBuiltFool/hair_trigger">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>
-->

<h3 align="center">Hair Trigger</h3>

  <p align="center">
    Simple, Subscribable, Luau-Style Events
    <br />
    <a href="https://github.com/BetterBuiltFool/hair_trigger"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <!--
    <a href="https://github.com/BetterBuiltFool/hair_trigger">View Demo</a>
    ·
    -->
    <a href="https://github.com/BetterBuiltFool/hair_trigger/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/BetterBuiltFool/hair_trigger/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
      <ul>
        <li><a href="#defining-events">Defining Events</a></li>
        <li><a href="#assigning-instances">Assigning Instances</a></li>
        <li><a href="#subscribing-to-events">Subscribing to Events</a></li>
        <li><a href="#triggering-events">Triggering Events</a></li>
        <li><a href="#synchronous-and-asynchronous">Synchronous and Asynchronous</a></li>
      </ul>
    <!-- <li><a href="#roadmap">Roadmap</a></li> -->
    <!--<li><a href="#contributing">Contributing</a></li>-->
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<!--
[![Product Name Screen Shot][product-screenshot]](https://example.com)
-->
TODO Project Name

Hair Trigger offers custom, subscribable events in the style of Luau events that allow for decoupled access between objects.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

Hair Trigger is written in pure python, with no system dependencies, and should be OS-agnostic.

### Installation

Hair Trigger can be installed from the [PyPI][pypi-url] using [pip][pip-url]:

```sh
pip install hair_trigger
```

and can be imported for use with:
```python
import hair_trigger
```

Hair Trigger has no dependencies beyond python itself.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Hair Trigger supplies no events by default, they must be custom made.

As an example, we'll make a simple event for detecting when an object is enabled.

### Defining Events


```python
from typing import Any
import hair_trigger

class OnEnable(hair_trigger.Event):
    """
    Called whenever the owner becomes enabled.

    :param this: The object being enabled.
    """

    def trigger(self, this: Any) -> None:
        return super().trigger(this)
```

Naming convention is suggested as `On[Event name]`. The `trigger` method must be defined, and must, at a minimum, call the super method. `trigger`s signature will also define the required signature of subscribing callbacks.
It is recommended to put the docstring describing `trigger`s parameters in the class docstring, so that it is visible to users.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Assigning Instances


Now we'll need an object to have the event.

```python

class Foo:
    def __init__(self, enabled:bool = False) -> None:
        self.OnEnable = OnEnable(self)
        self._enabled = enabled

```

When a `Foo` is created, a new instance of `OnEnable` is created for it, as well. The event attribute should be in Pascal case, matching the event class name, to ensure that users know it is an event and not a 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Subscribing to Events


Let's say we want to print something when a `Foo` is enabled. Subscribing is done by using the event instance as a decorator.


```python
foo = Foo()

@foo.OnEnable
def do_the_thing(this: Foo) -> None:
    print(f"{this} has been enabled")


# For simple expressions, a lambda is also okay
# For this though, we do not use it as a decorator.

foo.OnEnable(lambda this: print(f"{this} has been enabled"))

```

Additionally, objects can subscribe to an event as well. It uses the event as a decorator, too, but requires an additional parameter, typically the subscribing object. 

```python

class FooListener:

    def __init__(self, foo:Foo) -> None:

        @foo.OnEnable(self)
        def _(self, this:Foo) -> None:
            # Note: `self` here will shadow the `self` of init. This is important!
            print(f"{self} noticed {this} is now enabled")
```

If we have multiple of `FooListener`, the message will be printed once each.

Important notes:
- The callback should be defined in the init method.
- The callback does not need a name, "_" is fine.
- The `self` inside the callback must shadow the `self` of the init. This allows the callback to use the object, but won't prevent garbage collection due to a closure.
- Other than the `self`, the signature is _exactly the same_ as the trigger method of `OnEnable`.
- The owner of the callback doesn't have to be the subscribing object, just something that will live around the same lifetime.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Triggering Events

Now that we have a listener, we'll need to actually to something to trigger the event. To do this, we'll simply need to call the `trigger` method of the event.

```python

class Foo:
    # init definition as above

    @property
    def enabled(self) -> bool:
        return self._enabled
    
    @enabled.setter
    def enabled(self, enabled: bool) ->:
        self._enabled = enabled
        if enabled:
            self.OnEnable.trigger(self)
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Synchronous and Asynchronous

By default, Hair Trigger will attempt to run callbacks in synchronous mode. This means that any blocking that occurs in the callback will also block the main program. To get around this, you may use the `config` function to change the scheduler.

```python
import hair_trigger

hair_trigger.config(hair_trigger.SchedulingMode.THREADED)

```

There are three schedulers available:
- SyncScheduler: Corresponds to `SchedulingMode.DEFAULT`. Runs callbacks synchronously.
- ThreadScheduler: Corresponds to `SchedulingMode.THREADED`. Runs callbacks asynchronously using the python threading library.
- AsyncioScheduler: Corresponds to `SchedulingMode.ASYNCIO`. Runs callbacks asynchronously using the python asyncio library. This requires an asyncio loop already running, and all callbacks must be async-aware.

Additionally, custom schedulers may be created and passed alongside the `SchedulingMode.CUSTOM` enum.

```python

class LoggingThreadScheduler:

    def schedule(self, func: Callable[..., Any], *args, **kwds) -> None:
        print(f"Calling function {func}")
        threading.Thread(target=func, args=args, kwargs=kwds).start()


hair_trigger.config(hair_trigger.SchedulingMode.CUSTOM, LoggingThreadScheduler())

```




<!-- ROADMAP -->
<!-- ## Roadmap

- [ ] (Eternal) Improve the renderer. Faster rendering means more renderables! -->

<!--
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature
-->

<!-- See the [open issues](https://github.com/BetterBuiltFool/hair_trigger/issues) for a full list of proposed features (and known issues). -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
<!--
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

<a href="https://github.com/BetterBuiltFool/hair_trigger/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=BetterBuiltFool/hair_trigger" alt="contrib.rocks image" />
</a>
-->



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Better Built Fool - betterbuiltfool@gmail.com

Bluesky - [@betterbuiltfool.bsky.social](https://bsky.app/profile/betterbuiltfool.bsky.social)
<!--
 - [@twitter_handle](https://twitter.com/twitter_handle)
-->

Project Link: [https://github.com/BetterBuiltFool/hair_trigger](https://github.com/BetterBuiltFool/hair_trigger)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
<!--## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#readme-top">back to top</a>)</p>
-->


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/BetterBuiltFool/hair_trigger.svg?style=for-the-badge
[contributors-url]: https://github.com/BetterBuiltFool/hair_trigger/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/BetterBuiltFool/hair_trigger.svg?style=for-the-badge
[forks-url]: https://github.com/BetterBuiltFool/hair_trigger/network/members
[stars-shield]: https://img.shields.io/github/stars/BetterBuiltFool/hair_trigger.svg?style=for-the-badge
[stars-url]: https://github.com/BetterBuiltFool/hair_trigger/stargazers
[issues-shield]: https://img.shields.io/github/issues/BetterBuiltFool/hair_trigger.svg?style=for-the-badge
[issues-url]: https://github.com/BetterBuiltFool/hair_trigger/issues
[license-shield]: https://img.shields.io/github/license/BetterBuiltFool/hair_trigger.svg?style=for-the-badge
[license-url]: https://github.com/BetterBuiltFool/hair_trigger/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[python.org]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[python-url]: https://www.python.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
[pypi-url]: https://pypi.org/project/hair_trigger
[pip-url]: https://pip.pypa.io/en/stable/