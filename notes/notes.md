
Not all tests are fuzzing or smoke tests. 

Business impact: CI time, developer time running tests. Eventually in large
codebases, fatigue may set in due to setup and devs aren't writing tests.

1. The repetition of rerunning setup fixtures, unless explicitly asked, is repetitive
   and not valuable.
2. It's fine to cache side effects, even random ones, by default.

   If it's the intention to truly have fixtures that are fuzzy, this may also
   be possible in the future.
3. Having automatic faked results that are deterministic is useful.

   This means UUIDs or IDs that are in the order every time.


# 1. Cache the side effects of fixtures, not their return value

Caching in pytest normally inolves return responses.

However, the costliest tests to bootstrap aren't necessarily input / output
of calculations, they involve reading and writing, emitting and consuming,
and a end state a service should be in.

This tool will offer a flexible API where a cache hit quickly reproduces
a side effect, rather than rerunning the code 

This means potentially having to use an annotation of decorator to note
a fixture, such as a postgres one, that'd have a database value.

# 2. 
