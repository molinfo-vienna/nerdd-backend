# CHANGELOG


## v0.5.4 (2025-08-04)

### Fixes

* fix: Handle more errors in websocket connections ([`58a45af`](https://github.com/molinfo-vienna/nerdd-backend/commit/58a45afbf24bf71f7738c035ae1043561378f5e0))

### Unknown

* Merge pull request #56 from shirte/main

Handle more errors in websocket connections ([`da343a7`](https://github.com/molinfo-vienna/nerdd-backend/commit/da343a75010e1f5a7267c9a96ddbbaf226bac979))


## v0.5.3 (2025-08-04)

### Fixes

* fix: Use correct types in RethinkDbRepository ([`993a639`](https://github.com/molinfo-vienna/nerdd-backend/commit/993a639580f3240b655b2320d0bc9b5fc3e43fa4))

* fix: Improve performance of get_job_with_result_changes ([`b963138`](https://github.com/molinfo-vienna/nerdd-backend/commit/b963138c4bc2f3902502edf988af63eece470395))

* fix: Add deepcopy method to CompressedSet ([`94a33be`](https://github.com/molinfo-vienna/nerdd-backend/commit/94a33be7e699c2480f02e959afa4c6bf73a5a246))

### Unknown

* Merge pull request #55 from shirte/main

Improve performance of job status streaming significantly ([`94ea79a`](https://github.com/molinfo-vienna/nerdd-backend/commit/94ea79a894177ab28f1506d1db3616ad6c097f67))


## v0.5.2 (2025-08-01)

### Fixes

* fix: Catch RecordAlreadyExists error when saving results ([`2ace3d0`](https://github.com/molinfo-vienna/nerdd-backend/commit/2ace3d0195eafcc2a66eaa975df140ca7c7e249f))

* fix: Return result instance in create_result ([`db091e8`](https://github.com/molinfo-vienna/nerdd-backend/commit/db091e81b8df824dc7796c035abb2ad46945f605))

* fix: Save one update operation when saving results ([`724d884`](https://github.com/molinfo-vienna/nerdd-backend/commit/724d884010afca12270963ed276255c5097b637f))

### Unknown

* Merge pull request #54 from shirte/main

Improve performance of result saving ([`b2f3ee4`](https://github.com/molinfo-vienna/nerdd-backend/commit/b2f3ee457648151d11e8c44f3ab99de782491c5b))


## v0.5.1 (2025-08-01)

### Fixes

* fix: Handle RecordNotFoundError in get_job_ws ([`6fd7ede`](https://github.com/molinfo-vienna/nerdd-backend/commit/6fd7ede5d623b9095a4b548f0b103f8fc0a23a31))

* fix: Use WebSocketException in websocket routes ([`5e0a3a1`](https://github.com/molinfo-vienna/nerdd-backend/commit/5e0a3a13f60503cbb130bf0fb0da20a45e06b6d0))

* fix: Handle client disconnect gracefully in websocket routes ([`06e2264`](https://github.com/molinfo-vienna/nerdd-backend/commit/06e2264386e936f7b261810c52e41041018e80b0))

* fix: Close websocket connections when exceptions are raised ([`df4ff8f`](https://github.com/molinfo-vienna/nerdd-backend/commit/df4ff8f9c9af0fd68ef06e320766c40242de5e2e))

### Unknown

* Merge pull request #53 from shirte/main

Improve error handling in websockets ([`6263123`](https://github.com/molinfo-vienna/nerdd-backend/commit/6263123d9085ff4e2918da45cac9e22a76f511ac))


## v0.5.0 (2025-08-01)

### Features

* feat: Include TrackPredictionSpeed in main ([`c6d53be`](https://github.com/molinfo-vienna/nerdd-backend/commit/c6d53be36984305017bbe1efa8f81aabc7831263))

### Fixes

* fix: Log update in prediction time ([`978d8a7`](https://github.com/molinfo-vienna/nerdd-backend/commit/978d8a70fcc1eba309ae18827c1115c08dfc16c4))

* fix: Implement TrackPredictionSpeed action ([`1267e85`](https://github.com/molinfo-vienna/nerdd-backend/commit/1267e857446b346dc3551330c5e088a5ad57653f))

* fix: Add sklearn dependency ([`15351cd`](https://github.com/molinfo-vienna/nerdd-backend/commit/15351cdb45bf2e942700a31d13b96b7ebdb30feb))

* fix: Rename field in Module for consistency ([`1a93e24`](https://github.com/molinfo-vienna/nerdd-backend/commit/1a93e2489076a700e135ea2c55804c0db843a048))

* fix: Add new result checkpoint fields to compute prediction speed ([`92ce690`](https://github.com/molinfo-vienna/nerdd-backend/commit/92ce6904b348a1ac0edc2a54880e68f90c6588b9))

* fix: Add new job fields to compute prediction speed ([`3073bad`](https://github.com/molinfo-vienna/nerdd-backend/commit/3073bade1269435ec2cc507ceee3c272eca95da2))

* fix: Store job type in ResultCheckpoint ([`8e0042f`](https://github.com/molinfo-vienna/nerdd-backend/commit/8e0042fea1923e0e3c20aef286462d5fa2d75ca6))

* fix: Implement new repository methods in RethinkDbRepository ([`6de43ad`](https://github.com/molinfo-vienna/nerdd-backend/commit/6de43ad3d45ce225585df341bca5c1e69c6fba8c))

* fix: Implement new repository methods in MemoryRepository ([`dc56cfa`](https://github.com/molinfo-vienna/nerdd-backend/commit/dc56cfaeacd1714f2da0a5a10b8c66aea40beac9))

* fix: Add more checkpoint repository methods ([`06df45f`](https://github.com/molinfo-vienna/nerdd-backend/commit/06df45fbbfe9b6fdc87fdfb6aeef2b3e3fa9c260))

* fix: Adapt module router to ModuleInternal ([`b2cf373`](https://github.com/molinfo-vienna/nerdd-backend/commit/b2cf3737264425a37e4b459b712cc4fe33072167))

* fix: Let repository classes use ModuleInternal ([`657cac8`](https://github.com/molinfo-vienna/nerdd-backend/commit/657cac8cb7add919e8a0e0a4a3378cd5a7c2a4ba))

* fix: Add ModuleInternal model ([`9bd45d7`](https://github.com/molinfo-vienna/nerdd-backend/commit/9bd45d72ebf9693f85480033dee4a4879e971be3))

### Unknown

* Merge pull request #52 from shirte/main

Track prediction speed in all modules ([`718453a`](https://github.com/molinfo-vienna/nerdd-backend/commit/718453a4c2316102cf7657632725dd523ddd6f0f))


## v0.4.11 (2025-07-31)

### Fixes

* fix: Adapt to nerdd-link 0.5.0 ([`00d8865`](https://github.com/molinfo-vienna/nerdd-backend/commit/00d8865b63385dd487e9a19a038e0865e7c5b519))

* fix: Bump dependencies ([`0439d79`](https://github.com/molinfo-vienna/nerdd-backend/commit/0439d79ba978e24f77845f9eb1c7081b3df5c918))

### Unknown

* Merge pull request #51 from shirte/main

Adapt to nerdd-link 0.5.0 ([`8d93316`](https://github.com/molinfo-vienna/nerdd-backend/commit/8d933168563cc0be42c686acead1fe1302cac33c))


## v0.4.10 (2025-07-31)

### Fixes

* fix: Run StartSerialization action in main ([`b14a4cb`](https://github.com/molinfo-vienna/nerdd-backend/commit/b14a4cb98f22e2731ebf691ee4647a255dab3978))

* fix: Extract serialization into separate action ([`ae79f87`](https://github.com/molinfo-vienna/nerdd-backend/commit/ae79f87123f92810889f70b1353370f035977d88))

* fix: Adapt actions to ResultCheckpoint model ([`f1370ed`](https://github.com/molinfo-vienna/nerdd-backend/commit/f1370edc1dd5bd5b50cf526acd3ca63d2986e797))

* fix: Export ResultCheckpoint model ([`c0c5871`](https://github.com/molinfo-vienna/nerdd-backend/commit/c0c58714671a521f26187c4aa43fdadcf2d42825))

* fix: Add an id field to ResultCheckpoint model ([`4d0da54`](https://github.com/molinfo-vienna/nerdd-backend/commit/4d0da54872c5cc049ea8f23c8d48c2892fad3357))

* fix: Implement result checkpoint methods in RethinkDbRepository ([`3d3fe23`](https://github.com/molinfo-vienna/nerdd-backend/commit/3d3fe23eac463fc648fa24de18a17e4110319181))

* fix: Implement result checkpoint methods in MemoryRepository ([`2d0d416`](https://github.com/molinfo-vienna/nerdd-backend/commit/2d0d416d40f8077ae7f2cecb9c1b08ab9ae85827))

* fix: Add repository methods for result checkpoints ([`659d137`](https://github.com/molinfo-vienna/nerdd-backend/commit/659d137ac1fc7fc436036146083108a698b42ac5))

* fix: Remove checkpoint update from update_job ([`652d651`](https://github.com/molinfo-vienna/nerdd-backend/commit/652d6510872a5fd16321bd846c68c3b5ab3d991e))

* fix: Create separate model for result checkpoints ([`d0c5080`](https://github.com/molinfo-vienna/nerdd-backend/commit/d0c50808e0f213a9cc4c19b3f92e841e539796d5))

### Unknown

* Merge pull request #50 from shirte/main

Change serialization workflow ([`e1c9878`](https://github.com/molinfo-vienna/nerdd-backend/commit/e1c9878085e6e0ef0187466f337a0839312a5dfe))


## v0.4.9 (2025-07-24)

### Fixes

* fix: Check file path before returning to user ([`66bf56b`](https://github.com/molinfo-vienna/nerdd-backend/commit/66bf56bdfa8fb9af3c3d4dc0bd0db033d1784fbe))

### Unknown

* Merge pull request #49 from shirte/main

fix: Check file path before returning to user ([`6bff116`](https://github.com/molinfo-vienna/nerdd-backend/commit/6bff116be408569ef99239c50af7c44268884e6c))


## v0.4.8 (2025-07-24)

### Fixes

* fix: Use correct file path for large files ([`128660e`](https://github.com/molinfo-vienna/nerdd-backend/commit/128660e2b013f6713126aa9adbfe5eaa861238ed))

* fix: Bump dependencies ([`9135c48`](https://github.com/molinfo-vienna/nerdd-backend/commit/9135c48dd2ce1b7f92080da705b449f222419aaa))

* fix: Derive from Model instead of SimpleModel ([`7553d97`](https://github.com/molinfo-vienna/nerdd-backend/commit/7553d972e90eafab0e95c49f80a8158970ce15a4))

### Unknown

* Merge pull request #48 from shirte/main

Use correct path for large files ([`4a82481`](https://github.com/molinfo-vienna/nerdd-backend/commit/4a824818b1f9312027a936b5cd9a8887eddb14d5))


## v0.4.7 (2025-07-22)

### Fixes

* fix: Add default logo file ([`984cd0b`](https://github.com/molinfo-vienna/nerdd-backend/commit/984cd0bb7f8ecef5b8a4aeb5c35791d49b835a2f))

* fix: Exclude route for external files ([`0f2b0ce`](https://github.com/molinfo-vienna/nerdd-backend/commit/0f2b0ce034043c00f153c353b6ea832a53032757))

* fix: Serve module logos in separate route ([`e21a90b`](https://github.com/molinfo-vienna/nerdd-backend/commit/e21a90bcbb6ba58f5c18be95add4a5d86c0bfd65))

* fix: Exclude logo from module responses ([`320e476`](https://github.com/molinfo-vienna/nerdd-backend/commit/320e476eb1ff976dd6a5a8e1950e13198da77769))

### Unknown

* Merge pull request #47 from shirte/main

Speed up retrieval of module configurations ([`9b9102c`](https://github.com/molinfo-vienna/nerdd-backend/commit/9b9102c89c93533d3e40c015486cdd01c909abd8))


## v0.4.6 (2025-07-22)

### Fixes

* fix: Annotate return types in dynamic router ([`7a8de28`](https://github.com/molinfo-vienna/nerdd-backend/commit/7a8de2888f1c45d75bb9f4cbcfe4d785e03a39b0))

* fix: Annotate return types in modules router ([`8d03dfc`](https://github.com/molinfo-vienna/nerdd-backend/commit/8d03dfc8f864b32a4d3b8bd0c49803a054c13b0c))

* fix: Annotate return types in jobs router ([`a9bf812`](https://github.com/molinfo-vienna/nerdd-backend/commit/a9bf812384322db45272007cc10c3cbd434e8b0e))

* fix: Annotate return types in files router ([`8c723a5`](https://github.com/molinfo-vienna/nerdd-backend/commit/8c723a55bad3b6c6cff0c97872e84fba1eee6df5))

* fix: Annotate return types in challenges router ([`0c49145`](https://github.com/molinfo-vienna/nerdd-backend/commit/0c49145ea79a1e2f74beb8a030960f92ebb6333b))

* fix: Annotate return types in sources routes ([`6a4e5b5`](https://github.com/molinfo-vienna/nerdd-backend/commit/6a4e5b523a694e83e6a286b8a5df5d7e9dca4259))

* fix: Add BaseSuccessResponse class ([`30e7e53`](https://github.com/molinfo-vienna/nerdd-backend/commit/30e7e53dca34d530ba9a87677553f0b12e5f922e))

### Unknown

* Merge pull request #46 from shirte/main

Annotate return types in all routes ([`aa1ecf2`](https://github.com/molinfo-vienna/nerdd-backend/commit/aa1ecf26d320bfe086e313c04e29efe824365963))


## v0.4.5 (2025-07-14)

### Fixes

* fix: Return output_formats in /modules routes ([`26c595c`](https://github.com/molinfo-vienna/nerdd-backend/commit/26c595c00a279a711db6fa5cb67437667f4621ec))

* fix: Add output_formats to Module ([`08002b9`](https://github.com/molinfo-vienna/nerdd-backend/commit/08002b97a2af3911216dae62604cec76a77b5fd8))

* fix: Format copyright line ([`bf9f8b8`](https://github.com/molinfo-vienna/nerdd-backend/commit/bf9f8b80ec312d490f0c72bc23d3499f161af002))

* fix: Don't log requests in production ([`b198eae`](https://github.com/molinfo-vienna/nerdd-backend/commit/b198eae371fb73e4381d3d70cc02c2bbbb7830f9))

### Unknown

* Merge pull request #45 from shirte/main

Return available output formats in /modules requests ([`3d06c61`](https://github.com/molinfo-vienna/nerdd-backend/commit/3d06c6171930731cf7e9f28a0f7307d0e85f36dd))


## v0.4.4 (2025-07-13)

### Fixes

* fix: Use CORS middleware only in development mode ([`07194c3`](https://github.com/molinfo-vienna/nerdd-backend/commit/07194c30caa460f5bed0f836d1efea82b4db8937))

* fix: Use LogRequestsMiddleware if configured by user ([`6784478`](https://github.com/molinfo-vienna/nerdd-backend/commit/6784478a98e2cfac3f61a1dd5e8ab70a154fe604))

* fix: Implement LogRequestsMiddleware ([`2599a73`](https://github.com/molinfo-vienna/nerdd-backend/commit/2599a73b2a3d075ea96a20697dec503a3aff677f))

* fix: Check if mol_id bounds are None in MemoryRepository ([`359a189`](https://github.com/molinfo-vienna/nerdd-backend/commit/359a189ac45f0ba0c62f88983f6d1dcb1d847303))

### Unknown

* Merge pull request #44 from shirte/main

Reorganize fastapi middlewares ([`c369dd7`](https://github.com/molinfo-vienna/nerdd-backend/commit/c369dd7834edb391430f200e770080fe9526e19f))


## v0.4.3 (2025-07-12)

### Fixes

* fix: Use duplicate slash routes on websocket routes ([`2954796`](https://github.com/molinfo-vienna/nerdd-backend/commit/2954796819bd679afd168d3178a7ad41a58ca253))

* fix: Do not use root_path on uvicorn server ([`7f01603`](https://github.com/molinfo-vienna/nerdd-backend/commit/7f016036e8f65c5b80d4fbe263a49eba4eb10beb))

* fix: Remove trailing slashes in routes ([`d8810cb`](https://github.com/molinfo-vienna/nerdd-backend/commit/d8810cb86c6190752be53e21cb8514c013798a4f))

* fix: Remove redundant routes in challenges router ([`74b83b8`](https://github.com/molinfo-vienna/nerdd-backend/commit/74b83b8c1d9eb65413d9ba19336747936247c053))

* fix: Remove redundant routes in dynamic router ([`bcee419`](https://github.com/molinfo-vienna/nerdd-backend/commit/bcee419365b2ae8828ecbbc889af96bf78e97f0f))

* fix: Remove redundant routes in sources router ([`6c0498b`](https://github.com/molinfo-vienna/nerdd-backend/commit/6c0498b9a8a255eb2ec44e4e6186af0e3b7ce7a2))

* fix: Remove redundant routes in modules router ([`a23b00d`](https://github.com/molinfo-vienna/nerdd-backend/commit/a23b00dd542a72b03abc4995a7859dc5e61b5d1c))

* fix: Remove redundant routes in jobs router ([`dc2d6cc`](https://github.com/molinfo-vienna/nerdd-backend/commit/dc2d6ccd36e794b9e0006cf942d6bd5c77ca487b))

* fix: Remove redundant routes in websocket router ([`8aac664`](https://github.com/molinfo-vienna/nerdd-backend/commit/8aac664f5a502b110506b66d33092adc4dd53b49))

### Unknown

* Merge pull request #43 from shirte/main

Remove redundant fastapi routes ([`c19881c`](https://github.com/molinfo-vienna/nerdd-backend/commit/c19881ca2fba6327b28a7dd0d62724bf921442ad))


## v0.4.2 (2025-07-11)

### Code Style

* style: Check None in _create_job ([`50f1bf2`](https://github.com/molinfo-vienna/nerdd-backend/commit/50f1bf2d6f714c5a543aab5fbf9872c99d890c42))

### Fixes

* fix: Update version of fastapi ([`e000b0c`](https://github.com/molinfo-vienna/nerdd-backend/commit/e000b0cbc22962a1f827b5a8d7909273099f4058))

* fix: Omit deprecated job type check in _create_job function ([`a2c1a6a`](https://github.com/molinfo-vienna/nerdd-backend/commit/a2c1a6ad36293a8e5d2f62090694af0957e12aae))

* fix: Improve API structure for creating jobs ([`ff292e5`](https://github.com/molinfo-vienna/nerdd-backend/commit/ff292e5a16391282c61f6164f1eb3f46ba8276ac))

* fix: Add descriptions to fields ([`2b1578d`](https://github.com/molinfo-vienna/nerdd-backend/commit/2b1578d93222466daa908b9d542ace38383e1a96))

* fix: Compute valid model name by using snakecase before pascalcase ([`2abac8d`](https://github.com/molinfo-vienna/nerdd-backend/commit/2abac8d3d16bbcee61afe5e1e15c8dc9d8dcaa52))

### Unknown

* Merge pull request #42 from shirte/main

Improve API structure for creating jobs ([`6d292d7`](https://github.com/molinfo-vienna/nerdd-backend/commit/6d292d78205d63cccfea3f77e6ac157b101ac993))


## v0.4.1 (2025-07-09)

### Fixes

* fix: Add missing route to /modules router ([`ab58a55`](https://github.com/molinfo-vienna/nerdd-backend/commit/ab58a5508448d247adbf1827545200d6c70230c2))

* fix: Extract augment_module function ([`74702e4`](https://github.com/molinfo-vienna/nerdd-backend/commit/74702e40066330982a4dbf66f3595deb8cf47bb5))

### Unknown

* Merge pull request #41 from shirte/main

Extract augment_module function ([`cda868a`](https://github.com/molinfo-vienna/nerdd-backend/commit/cda868af20782ada80b663ee02e0e971a426fa23))


## v0.4.0 (2025-07-04)

### Documentation

* docs: Simplify readme ([`56e42e6`](https://github.com/molinfo-vienna/nerdd-backend/commit/56e42e61696413c9e060d7d0ad3d0af556d03135))

### Features

* feat: Implement job expiration in MemoryRepository ([`29496e4`](https://github.com/molinfo-vienna/nerdd-backend/commit/29496e408c09e4efe3a79d000dc901a3e41b5f26))

* feat: Require methods for obtaining expired jobs ([`a69fd68`](https://github.com/molinfo-vienna/nerdd-backend/commit/a69fd68a5cbe6d71e150c7cad55823c22824d03f))

### Fixes

* fix: Add config to specify job expiration ([`825e4d7`](https://github.com/molinfo-vienna/nerdd-backend/commit/825e4d776829385495e97cc112e3482870877047))

### Unknown

* Merge pull request #40 from shirte/main

Enable retrieving expired jobs ([`190bf75`](https://github.com/molinfo-vienna/nerdd-backend/commit/190bf75d569f6c49d898e5c6ccb91eb93ef1d886))

* Merge pull request #39 from shirte/main

docs: Simplify readme ([`09bad35`](https://github.com/molinfo-vienna/nerdd-backend/commit/09bad359aea320b023533b57c734a0ab494bc607))


## v0.3.0 (2025-07-03)

### Features

* feat: Simplify job updates using CompressedSet ([`6574cfd`](https://github.com/molinfo-vienna/nerdd-backend/commit/6574cfdb41be623bb145a3d2a15987ae868c8e7b))

### Fixes

* fix: Handle the case job_id does not exist in get_job_by_id ([`7b09e30`](https://github.com/molinfo-vienna/nerdd-backend/commit/7b09e3071238c0ee13308933636d4e74a07695b8))

* fix: Fix a typo in UpdateJobSize action ([`4ff0d36`](https://github.com/molinfo-vienna/nerdd-backend/commit/4ff0d369186a4d14992315e3b4983381d6ea3e0f))

* fix: Do not require deletion methods in repository yet ([`f2e992a`](https://github.com/molinfo-vienna/nerdd-backend/commit/f2e992ab9691ed3f7180645c0b919d5f4d69efef))

* fix: Fix a bug in repository ([`ed66d36`](https://github.com/molinfo-vienna/nerdd-backend/commit/ed66d36600dceb9449f7190553213afd970eaa19))

* fix: Merge correct intervals in add method ([`d5a3d66`](https://github.com/molinfo-vienna/nerdd-backend/commit/d5a3d66fec04cda3e6809f674469e1ffec8f9a23))

* fix: Adapt RethinkDbRepository to JobWithResults ([`0f5c80b`](https://github.com/molinfo-vienna/nerdd-backend/commit/0f5c80b3ad203f3de14f3916ac9c09dd7da4534a))

* fix: Adapt MemoryRepository to JobWithResults ([`78a1328`](https://github.com/molinfo-vienna/nerdd-backend/commit/78a1328c71cba13e00bdd0a950cad320d93300dc))

* fix: Implement get_job_with_result_changes ([`eef3fe3`](https://github.com/molinfo-vienna/nerdd-backend/commit/eef3fe3758f3f56b602d33a6fcf8b6a1e7eaf09c))

* fix: Add is_done method on job model ([`e1331f5`](https://github.com/molinfo-vienna/nerdd-backend/commit/e1331f56ec42db7b55c2b3b6e488c15e68c42567))

* fix: Implement union operation on CompressedSet ([`db94421`](https://github.com/molinfo-vienna/nerdd-backend/commit/db94421850b9eb095f9e92f9c0cd73328adcd8c1))

* fix: Use model JobWithResults in jobs router ([`4bcec64`](https://github.com/molinfo-vienna/nerdd-backend/commit/4bcec64ece235654ee56bba0b614a8fb831e7a9e))

* fix: Create new model JobWithResults ([`294114f`](https://github.com/molinfo-vienna/nerdd-backend/commit/294114f96b4e110a3f047cfe36e9fbe7ba411338))

* fix: Make CompressedSet serializable ([`c5e69e7`](https://github.com/molinfo-vienna/nerdd-backend/commit/c5e69e78d534b5fe5352e27229f7998878292a80))

* fix: Correct typo in CompressedSet ([`18f9fe7`](https://github.com/molinfo-vienna/nerdd-backend/commit/18f9fe77c3e6fdd14e329f89503d2291a71e14bd))

* fix: Handle invalid input to CompressedSet constructor ([`d899c49`](https://github.com/molinfo-vienna/nerdd-backend/commit/d899c49914208d5943071a7cd793dd4405b19a5e))

* fix: Implement CompressedSet.contains ([`f2f50c5`](https://github.com/molinfo-vienna/nerdd-backend/commit/f2f50c552ecb19234fe723ca2b806c7672e9e0af))

* fix: Extend constructor of CompressedSet ([`4bccd60`](https://github.com/molinfo-vienna/nerdd-backend/commit/4bccd603228947293e404bd585851287096aeab1))

### Testing

* test: Add tests for empty constructor arguments in CompressedSet ([`2acd2d4`](https://github.com/molinfo-vienna/nerdd-backend/commit/2acd2d47ba7386ee99cc6aa59f2b7d49286482a1))

* test: Allow CompressedSet as constructor argument in CompressedSet ([`5e40875`](https://github.com/molinfo-vienna/nerdd-backend/commit/5e40875950a89f468e46fb36ae9e97122f56dbeb))

* test: Add tests for CompressedSet using larger inputs ([`39635fd`](https://github.com/molinfo-vienna/nerdd-backend/commit/39635fd2103a5d62fd54c044aac4c5b203f82248))

* test: Add test for CompressedSet.union ([`7a1dde5`](https://github.com/molinfo-vienna/nerdd-backend/commit/7a1dde51ece594f088f33cc66d150c09de9f8a58))

* test: Add tests for CompressedSet ([`5b26601`](https://github.com/molinfo-vienna/nerdd-backend/commit/5b26601fb918a39f7c7ba6b41769a422cbfc22a7))

### Unknown

* Merge pull request #38 from shirte/main

Simplify (and speed up) job updates using CompressedSet ([`65fb703`](https://github.com/molinfo-vienna/nerdd-backend/commit/65fb70371adcfd7a1cf0d395157b5950af1cee27))


## v0.2.4 (2025-06-30)

### Fixes

* fix: Delete output files on deletion request ([`8565b5f`](https://github.com/molinfo-vienna/nerdd-backend/commit/8565b5f23dc709c3fb01d8d81ae662fb1f03b7bc))

* fix: Handle deleted jobs in UpdateJobSize ([`0a67265`](https://github.com/molinfo-vienna/nerdd-backend/commit/0a67265c0784450d0bb13d57dadfbdf93e82a318))

* fix: Handle deleted jobs in SaveResult ([`f48d406`](https://github.com/molinfo-vienna/nerdd-backend/commit/f48d40695a50f77ff9da533deb812cb898003ac6))

* fix: Handle deleted jobs in SaveResultCheckpointToDb ([`b5963f6`](https://github.com/molinfo-vienna/nerdd-backend/commit/b5963f606504ae2da0fff23c8075bdc128501e5d))

* fix: Handle deleted jobs in ProcessSerializationResult ([`1c15665`](https://github.com/molinfo-vienna/nerdd-backend/commit/1c1566568156685613e4a747cd8a5bdf4100eb8e))

* fix: Propagate job deletion to kafka ([`083a62c`](https://github.com/molinfo-vienna/nerdd-backend/commit/083a62cad0288840bdfc61bb24c51ae4855191a0))

### Unknown

* Merge pull request #37 from shirte/main

Handle deleted jobs ([`9a28fd1`](https://github.com/molinfo-vienna/nerdd-backend/commit/9a28fd10efe994e553b489ce5b52664bf6203352))


## v0.2.3 (2025-06-30)

### Fixes

* fix: Do not import example model from test packages ([`243c7cf`](https://github.com/molinfo-vienna/nerdd-backend/commit/243c7cfe8c368445f8c237f78b3e55cb5b960911))

### Unknown

* Merge pull request #36 from shirte/main

fix: Do not import example model from test packages ([`77b2c85`](https://github.com/molinfo-vienna/nerdd-backend/commit/77b2c851a17e7d7fb287d55f67055ec6b3960b13))


## v0.2.2 (2025-06-28)

### Fixes

* fix: Add folders to gitignore ([`58e2d2b`](https://github.com/molinfo-vienna/nerdd-backend/commit/58e2d2b5d528bae9fa305ea2475a4fb323ecc3fd))

* fix: Add development Dockerfile ([`33c4d0d`](https://github.com/molinfo-vienna/nerdd-backend/commit/33c4d0d414fcf8273c7b776b0341d9a54eab49a4))

* fix: Update nerdd-link ([`82a1e79`](https://github.com/molinfo-vienna/nerdd-backend/commit/82a1e792ff62473353736afabf2b262c9ba7a051))

### Unknown

* Merge pull request #35 from shirte/main

Update nerdd-link ([`c4ede62`](https://github.com/molinfo-vienna/nerdd-backend/commit/c4ede6253188f2ccab5985d9c043639d5823711e))


## v0.2.1 (2025-06-26)

### Code Style

* style: Adapt import directives ([`fd8ec0e`](https://github.com/molinfo-vienna/nerdd-backend/commit/fd8ec0e20efb68fa462500a52376c743ad576f6f))

* style: Use async_step from nerdd-link ([`9b94a54`](https://github.com/molinfo-vienna/nerdd-backend/commit/9b94a542439103c198d33136f4726dcf4b3b7bc7))

* style: Remove unused dependency 'time' in SaveResultsToDb ([`f1aca27`](https://github.com/molinfo-vienna/nerdd-backend/commit/f1aca27638da78b7beaad944e930d28421884ce5))

* style: Remove unused code in RethinkDbRepository ([`7ab4f9d`](https://github.com/molinfo-vienna/nerdd-backend/commit/7ab4f9d7fa3662a04491c679a8ec0828bfba9931))

### Fixes

* fix: pytest-bdd required for normal runs (ie non dev/test), adding to requirements.txt ([`ca06182`](https://github.com/molinfo-vienna/nerdd-backend/commit/ca0618209284c39a6542de210115a89b19e0445f))

### Unknown

* Merge pull request #34 from wschuell/main

fix: pytest-bdd required for normal runs (ie non dev/test), adding to… ([`6897c19`](https://github.com/molinfo-vienna/nerdd-backend/commit/6897c1971b0992aae897f5788909b7e03ef1c644))

* Merge pull request #33 from shirte/main

Cosmetic changes ([`ccd70c0`](https://github.com/molinfo-vienna/nerdd-backend/commit/ccd70c0e8f8386850c0b7a4211cc850c57e5dbea))


## v0.2.0 (2025-06-10)

### Features

* feat: Add challenge router to main ([`cc444cc`](https://github.com/molinfo-vienna/nerdd-backend/commit/cc444cc1e8ec85c64e527ae0229fa4d692b0a755))

* feat: Implement challenges router ([`68b7e05`](https://github.com/molinfo-vienna/nerdd-backend/commit/68b7e05a291c6f968d25897f5b4a57a1569ec00a))

### Fixes

* fix: Add timezone to challenge expiration dates ([`d2e0fa7`](https://github.com/molinfo-vienna/nerdd-backend/commit/d2e0fa764ad9dbed3005a3e5dd1db6524fb61e6b))

* fix: Create challenges table ([`8fb34ad`](https://github.com/molinfo-vienna/nerdd-backend/commit/8fb34ade718dd0c7b46904b2a58b4536fe89574a))

* fix: Provide challenge parameters in config files ([`097f1c0`](https://github.com/molinfo-vienna/nerdd-backend/commit/097f1c0ea951475437a4b010816a4b74768bccbe))

* fix: Implement challenge methods in RethinkDbRepository ([`01c3fef`](https://github.com/molinfo-vienna/nerdd-backend/commit/01c3fef7ffb74f1d314d79712ac5d0887c563d2f))

* fix: Implement challenge methods in MemoryRepository ([`dd49598`](https://github.com/molinfo-vienna/nerdd-backend/commit/dd4959838d8b08c47a7aff3f00de89680338be99))

* fix: Add altcha challenge model ([`025c84e`](https://github.com/molinfo-vienna/nerdd-backend/commit/025c84e3ccefc0881d8b08198f58412f2ff4e299))

* fix: Add repository methods for altcha challenges ([`a8b28c1`](https://github.com/molinfo-vienna/nerdd-backend/commit/a8b28c106d8913d88f775f89c259ea04b5fa05a9))

* fix: Add altcha dependency ([`2509d6f`](https://github.com/molinfo-vienna/nerdd-backend/commit/2509d6f6e30ae9e0f6d7d6cf076ed06515ad1bc6))

### Unknown

* Merge pull request #32 from shirte/main

Introduce altcha challenges ([`b0430f9`](https://github.com/molinfo-vienna/nerdd-backend/commit/b0430f956c9ae579483155e74900fd39c9300f7c))


## v0.1.1 (2025-06-09)

### Fixes

* fix: Accept referer header and store in job records ([`bce4dcd`](https://github.com/molinfo-vienna/nerdd-backend/commit/bce4dcde35bdc68239666f69eecc7a4d74f39304))

* fix: Add referer field to JobInternal model ([`2ebc586`](https://github.com/molinfo-vienna/nerdd-backend/commit/2ebc5864391288d2b167eefc05f04b381cb72049))

* fix: Use JobInternal instead of Job model in create_job ([`52278f2`](https://github.com/molinfo-vienna/nerdd-backend/commit/52278f2b05ef8b8a9bfdf17962afd6b0a37cc3a8))

### Unknown

* Merge pull request #31 from shirte/main

Accept referer header and store in job records ([`99e8c30`](https://github.com/molinfo-vienna/nerdd-backend/commit/99e8c30eabf43a60ff015dfda26351c0734b26b3))


## v0.1.0 (2025-06-09)

### Code Style

* style: Use ./media as the test media directory ([`4d0cd53`](https://github.com/molinfo-vienna/nerdd-backend/commit/4d0cd53d38d62d3380be7bee7857573ebe01f7e6))

### Features

* feat: Implement quota check ([`2fed40d`](https://github.com/molinfo-vienna/nerdd-backend/commit/2fed40dc92f71abf19c2dd3f1b1fc08422775923))

* feat: Add user_id field to job model ([`cd8a92c`](https://github.com/molinfo-vienna/nerdd-backend/commit/cd8a92ce8e23f5745de03f2ed6ef2289e25d575a))

* feat: Add user model ([`7d8b5b6`](https://github.com/molinfo-vienna/nerdd-backend/commit/7d8b5b647f4dc302bca78e1d7b500179e01fb8a8))

### Fixes

* fix: Use CLI args in Dockerfile ([`2085e5b`](https://github.com/molinfo-vienna/nerdd-backend/commit/2085e5b8ed3b07f551fb96eeaf70e0441db013ef))

* fix: Implement repository methods in RethinkDbRepository ([`35c16fc`](https://github.com/molinfo-vienna/nerdd-backend/commit/35c16fcd8a50fa3d6e82cacbd0730425bca73c14))

* fix: Implement repository methods in MemoryRepository ([`d31ed31`](https://github.com/molinfo-vienna/nerdd-backend/commit/d31ed315876cf9791c7875cb9f5b17c6756991f8))

* fix: Define repository methods for users ([`4c591e5`](https://github.com/molinfo-vienna/nerdd-backend/commit/4c591e554ab2cb736ef87cfb23e6358a5166c7a6))

* fix: Check user quota on job creation ([`eb4c52d`](https://github.com/molinfo-vienna/nerdd-backend/commit/eb4c52d225261297fe4e3ec2ee9079dc313b4184))

* fix: Add quota field to configs ([`0cc16b1`](https://github.com/molinfo-vienna/nerdd-backend/commit/0cc16b1f79baabb7bfff801ba7ffc3ae68e6af3b))

* fix: Fix typo ([`7f389ed`](https://github.com/molinfo-vienna/nerdd-backend/commit/7f389ed7de59ccf90ac5474d8215094e1a9da569))

* fix: Simplify files parameter in create_complex_job routes ([`5e760ea`](https://github.com/molinfo-vienna/nerdd-backend/commit/5e760ea6b80f1399e767de5f97fdd3e9042c03e0))

* fix: Process source files correctly ([`ac4347d`](https://github.com/molinfo-vienna/nerdd-backend/commit/ac4347d0beb4cdafcb8508005bde928431cfa5ab))

* fix: Use None when encountering invalid sources ([`4af5d05`](https://github.com/molinfo-vienna/nerdd-backend/commit/4af5d05871e3ef4c9793c3506bf97b0d0a70d807))

* fix: Add ./data to gitignore ([`3da26e2`](https://github.com/molinfo-vienna/nerdd-backend/commit/3da26e28b7589935a88236eed9524c15a7148626))

* fix: Read api base path from config ([`3721b07`](https://github.com/molinfo-vienna/nerdd-backend/commit/3721b0788586c8d763b5e7afe81571172c7517b3))

### Unknown

* Merge pull request #30 from shirte/main

Add quota check ([`aac04f6`](https://github.com/molinfo-vienna/nerdd-backend/commit/aac04f60b5d4007f2fe9890f9c9e6be4fef56614))


## v0.0.9 (2025-05-24)

### Fixes

* fix: Let fastapi figure out urls in response objects ([`35b350c`](https://github.com/molinfo-vienna/nerdd-backend/commit/35b350cfbd8b3965b89977df2ae6bc018b215903))

* fix: Make fastapi aware of proxy headers ([`fe5ae62`](https://github.com/molinfo-vienna/nerdd-backend/commit/fe5ae62572ca136a2821532ae5057d8b328879a7))

* fix: Fix typo ([`2c16f32`](https://github.com/molinfo-vienna/nerdd-backend/commit/2c16f3279652e2240e9a814dbaad34cad965491e))

* fix: Add routes with trailing slash ([`c2ff026`](https://github.com/molinfo-vienna/nerdd-backend/commit/c2ff02610bd303de09d558e597b5ae29e759de43))

### Unknown

* Merge pull request #29 from shirte/main

Make fastapi aware of proxy headers ([`a20c066`](https://github.com/molinfo-vienna/nerdd-backend/commit/a20c0666b690deb06a2a3f4e746c1019143aa326))


## v0.0.8 (2025-05-23)

### Fixes

* fix: Update Dockerfile with more generic image to support arm64 ([`d81fe42`](https://github.com/molinfo-vienna/nerdd-backend/commit/d81fe42872dbbdf5459ef7179c52698b2b50ee6a))


## v0.0.7 (2025-05-23)

### Fixes

* fix: Update build-container.yml to support arm64 ([`6e151d3`](https://github.com/molinfo-vienna/nerdd-backend/commit/6e151d304c68b673c2fd10e198d1f092c3bfb039))

### Unknown

* Update build-container.yml to support arm64 ([`eb029e3`](https://github.com/molinfo-vienna/nerdd-backend/commit/eb029e3a4ec1d9f90e25778cd641c2396855ba97))


## v0.0.6 (2025-04-17)

### Fixes

* fix: Bump version of nerdd-module and nerdd-link ([`02ef0dd`](https://github.com/molinfo-vienna/nerdd-backend/commit/02ef0dd565a1a7ec50d96bf573b19256311f5a2f))

* fix: Rewrite file paths of large properties ([`f617e26`](https://github.com/molinfo-vienna/nerdd-backend/commit/f617e26a9392b74978d053f460cd908c904f2637))

* fix: Add file router to main ([`42f45ab`](https://github.com/molinfo-vienna/nerdd-backend/commit/42f45ab55e0a827a8f691a39a5e07a8eb7bb25a8))

* fix: Implement file router ([`61204c8`](https://github.com/molinfo-vienna/nerdd-backend/commit/61204c844dcc03e428c7167fa73458038bc12bea))

### Unknown

* Merge pull request #28 from shirte/main

Handle file paths of large properties that were stored on disk ([`2f9a134`](https://github.com/molinfo-vienna/nerdd-backend/commit/2f9a134967e135b0646913369ae9448fd772a681))


## v0.0.5 (2025-04-12)

### Fixes

* fix: Remove looseversion dependency (since rethinkdb fixed that) ([`de42294`](https://github.com/molinfo-vienna/nerdd-backend/commit/de42294139acb34fd818be5d51ddb41be07f7436))

* fix: Update Python to 3.12 ([`4ccfe99`](https://github.com/molinfo-vienna/nerdd-backend/commit/4ccfe994470080c35ad791126f4efff77c5affc7))

* fix: Update rethinkdb dependency ([`2c409a6`](https://github.com/molinfo-vienna/nerdd-backend/commit/2c409a6f9e4edc14183634b17e8338061ac3fc37))

### Unknown

* Merge pull request #27 from shirte/main

Update rethinkdb dependency ([`03b96a6`](https://github.com/molinfo-vienna/nerdd-backend/commit/03b96a6049e5545fdb693ddba9b6690e7f52e6c2))


## v0.0.4 (2025-04-02)

### Fixes

* fix: Use uvicorn[standard] in requirements.txt ([`3043d52`](https://github.com/molinfo-vienna/nerdd-backend/commit/3043d5210c5dd65818da42770cac0501dff5f266))

* fix: Bump version of nerdd-module in pyproject.toml ([`fd298a7`](https://github.com/molinfo-vienna/nerdd-backend/commit/fd298a7e9b6b3d30d7c0211e96b20e16be719b51))

### Unknown

* Merge pull request #26 from shirte/main

Use uvicorn[standard] in requirements.txt ([`0b4e592`](https://github.com/molinfo-vienna/nerdd-backend/commit/0b4e5928258a369004e8d5abf7e0aa25b4b01a0e))

* Remove unnecessary dependencies ([`b9dec2d`](https://github.com/molinfo-vienna/nerdd-backend/commit/b9dec2d9c58ec1d1babc03a6b23123af5488ca92))


## v0.0.3 (2025-03-30)

### Fixes

* fix: Bump version of nerdd-module ([`ca76d79`](https://github.com/molinfo-vienna/nerdd-backend/commit/ca76d79dea766deafd29ff319c8d6f00f0aa5eab))

### Unknown

* Merge pull request #25 from shirte/main

fix: Bump version of nerdd-module ([`e4c0a85`](https://github.com/molinfo-vienna/nerdd-backend/commit/e4c0a85bfdd4059e32717c652bc50add338fb38d))


## v0.0.2 (2025-03-29)

### Fixes

* fix: Extend dockerignore file ([`7712747`](https://github.com/molinfo-vienna/nerdd-backend/commit/77127479a964d5f661c5a8d75f308e4090ac83af))

* fix: Adapt Dockerfile ([`f2ebf27`](https://github.com/molinfo-vienna/nerdd-backend/commit/f2ebf27689d58bdc3d40c6a5b034b5403bdcfaa6))

* fix: Add requirements.txt ([`26b85a4`](https://github.com/molinfo-vienna/nerdd-backend/commit/26b85a44b46acbc777caeefc93ddcb2e3e366f53))

* fix: Delete contradicting license terms ([`e26ae60`](https://github.com/molinfo-vienna/nerdd-backend/commit/e26ae6099557ddb4399cf166df9bca023d072f3d))

### Unknown

* Merge pull request #24 from shirte/main

Add requirements.txt ([`835e671`](https://github.com/molinfo-vienna/nerdd-backend/commit/835e671eb055ead2f5bdde432228d710294f3939))

* Merge pull request #23 from shirte/main

Add contribution section to readme file ([`0c630f6`](https://github.com/molinfo-vienna/nerdd-backend/commit/0c630f663b4fabbcc154ff08e99bf768af7e36b6))

* Use pytest-watcher instead of pytest-watch ([`988d662`](https://github.com/molinfo-vienna/nerdd-backend/commit/988d662e9d84eca5de184aff6f27d41c42b9b568))

* Add section on unit testing ([`2d4110d`](https://github.com/molinfo-vienna/nerdd-backend/commit/2d4110db77bebb6ff2c49246ae4a6461e70f44eb))

* Add hint on api access in contribution section ([`88fb181`](https://github.com/molinfo-vienna/nerdd-backend/commit/88fb1815abee373a4233615bb7ffa1974a2278b9))

* Add missing dependency in contribution section ([`0687d1b`](https://github.com/molinfo-vienna/nerdd-backend/commit/0687d1bd4a3df33b93fbc8f4ecaed129e5a25363))

* Add contribution section to readme ([`bcd65c9`](https://github.com/molinfo-vienna/nerdd-backend/commit/bcd65c9ecccafafc44dbbb1109ff032ed280b04f))


## v0.0.1 (2025-02-07)

### Fixes

* fix: Change image repository ([`5b819d1`](https://github.com/molinfo-vienna/nerdd-backend/commit/5b819d1767db550d04b8fca0b95f2935ef9b93a9))

* fix: Improve performance by caching sources ([`64685aa`](https://github.com/molinfo-vienna/nerdd-backend/commit/64685aae76b24c01dbfc7677290be97b2541e6c7))

* fix: Add dockerignore ([`c4ad96d`](https://github.com/molinfo-vienna/nerdd-backend/commit/c4ad96d8cd89b23523825f31ae0c5c2f433a5e85))

* fix: Set page size in production to 100 ([`fd5856c`](https://github.com/molinfo-vienna/nerdd-backend/commit/fd5856cefcc7d66814ecec324580e4e2619f5a7c))

* fix: Remove manual check of env variables ([`cd21eed`](https://github.com/molinfo-vienna/nerdd-backend/commit/cd21eed899aa1e8302c3572d713318c86fd121d8))

* fix: Fix errors ([`f284651`](https://github.com/molinfo-vienna/nerdd-backend/commit/f28465150678803b4e7634a6f34838fe40fde229))

* fix: Fix problems in RethinkDbRepository ([`d0b391a`](https://github.com/molinfo-vienna/nerdd-backend/commit/d0b391a79ed901f160481a0f00e950212a9fb2e8))

* fix: Specify timezones in models ([`b84ec8a`](https://github.com/molinfo-vienna/nerdd-backend/commit/b84ec8a1f38319cc035f25648c148356e99c5c8e))

* fix: Load all modules on startup ([`60f9145`](https://github.com/molinfo-vienna/nerdd-backend/commit/60f9145cd4bf6bb9587ef43ff05473448ce1ef29))

### Unknown

* Merge pull request #22 from shirte/main

Make cache thread-safe ([`1dfdcb9`](https://github.com/molinfo-vienna/nerdd-backend/commit/1dfdcb9cd1e4354c3f431f9a7924c5b16902a1bf))

* Make source cache thread-safe ([`0e401f5`](https://github.com/molinfo-vienna/nerdd-backend/commit/0e401f5f20881c8380084d8e8a966ee10e76d4b0))

* Merge pull request #21 from shirte/main

Add semantic release ([`ca9ebe0`](https://github.com/molinfo-vienna/nerdd-backend/commit/ca9ebe09e8ead79a881678ee4e350d30c5c5a4af))

* Do not run semantic release on forks ([`99b9948`](https://github.com/molinfo-vienna/nerdd-backend/commit/99b9948d660e02b2aed437f676eea728ef12985d))

* Build docker container on new release ([`95c54b0`](https://github.com/molinfo-vienna/nerdd-backend/commit/95c54b00b40d1aa5baec0833e1cf6026e99dacba))

* Configure pyproject.toml for semantic release ([`52ffd3b`](https://github.com/molinfo-vienna/nerdd-backend/commit/52ffd3b03d4bee44a1e2093ee0c53c13022df13e))

* Add github action for semantic release ([`1d9bc2f`](https://github.com/molinfo-vienna/nerdd-backend/commit/1d9bc2f1f1e4056baf188ffb2dc0cd0049f43cea))

* Add dockerfile ([`29ca590`](https://github.com/molinfo-vienna/nerdd-backend/commit/29ca59056b9ea563e529b15a1c90c794f2b7f0e9))

* Remove defaults channel from conda env ([`8f58b85`](https://github.com/molinfo-vienna/nerdd-backend/commit/8f58b85e9ae730ddebd215a4ae3ee4068d6756bf))

* Merge pull request #20 from shirte/main

Make all queries atomic ([`a79b728`](https://github.com/molinfo-vienna/nerdd-backend/commit/a79b728ee1de76827c2e4ab064f1f881fc73349a))

* Add dockerfile ([`8c1a067`](https://github.com/molinfo-vienna/nerdd-backend/commit/8c1a0679be5362fbaee4bfbdb326e0d69352edd1))

* Make all queries atomic ([`0024c26`](https://github.com/molinfo-vienna/nerdd-backend/commit/0024c261d81b8568d9b5673dbead8067af4a7418))

* Remove pip dependency in conda env ([`3f85163`](https://github.com/molinfo-vienna/nerdd-backend/commit/3f85163e15374c23ce826fd478aa8531f272d627))

* Add secondary index on job_id to results table ([`78a8b9f`](https://github.com/molinfo-vienna/nerdd-backend/commit/78a8b9ff0cd522254ece160a0ce6004c12580c2f))

* Merge pull request #19 from shirte/main

Add gzip compression middleware ([`69babf1`](https://github.com/molinfo-vienna/nerdd-backend/commit/69babf1daf66001239b873f0bc8ae2dd7aae7db8))

* Hide modules when visible is set to false ([`1b4839c`](https://github.com/molinfo-vienna/nerdd-backend/commit/1b4839ca6769aa21ce72a59f9c26d934667247fc))

* Add gzip compression middleware ([`d7a9943`](https://github.com/molinfo-vienna/nerdd-backend/commit/d7a9943bd4c4c8e906b8a28f81ed6a239aafbbd1))

* Use compressed sets to store processed entries ([`7b827c9`](https://github.com/molinfo-vienna/nerdd-backend/commit/7b827c9373c1bcbb50aead4704e6c03ec5e99e5e))

* Let page size depend on model ([`2a24130`](https://github.com/molinfo-vienna/nerdd-backend/commit/2a241300139e4961e918d2c94068344fd7176db6))

* Merge pull request #18 from shirte/main

Minor changes ([`a4b8f0e`](https://github.com/molinfo-vienna/nerdd-backend/commit/a4b8f0ec5c7820737283c416b7ee56cfe85581a7))

* Use correct urls for file downloads ([`0468ef7`](https://github.com/molinfo-vienna/nerdd-backend/commit/0468ef77a7a0309c93c6f1fe87fd51aa971a16cd))

* Map sources to their original upload names ([`076ce76`](https://github.com/molinfo-vienna/nerdd-backend/commit/076ce765df210351f0cbe47e2d4b2fe238fb0952))

* Return correct value if module did not change ([`e8e5e3b`](https://github.com/molinfo-vienna/nerdd-backend/commit/e8e5e3bdf5189a53006acf264720d14758a68f12))

* Check if job exists before adding results ([`39ca343`](https://github.com/molinfo-vienna/nerdd-backend/commit/39ca3432f3840fbb845af892b041efa6ea92f46f))

* Update job.num_entries_processed when new results arrive ([`8423e8b`](https://github.com/molinfo-vienna/nerdd-backend/commit/8423e8b372f862364a1412367fb66a3319eb1796))

* Merge pull request #17 from shirte/main

Improve production settings ([`a2cc0f8`](https://github.com/molinfo-vienna/nerdd-backend/commit/a2cc0f83628638abc604165ae5b0385f77d40a89))

* Fix results websocket ([`57ba444`](https://github.com/molinfo-vienna/nerdd-backend/commit/57ba44458a521150a72c7f970e685c8e4e3775e3))

* Implement update_module ([`a542fcf`](https://github.com/molinfo-vienna/nerdd-backend/commit/a542fcfa2cad4ace5d84ba945db9b3956dc78283))

* Enable updating modules ([`f7dcf84`](https://github.com/molinfo-vienna/nerdd-backend/commit/f7dcf84b6d84588a71a05ec547c29857be8618f5))

* Simplify dockerignore file ([`b769a2c`](https://github.com/molinfo-vienna/nerdd-backend/commit/b769a2cc138111ea3a4db6ad58865f08df507976))

* Adapt serialization topic and listeners to new version ([`23d97c4`](https://github.com/molinfo-vienna/nerdd-backend/commit/23d97c4f41332f1f122213b88f9f4b0b936ee96a))

* Add more allowed origins ([`7c54831`](https://github.com/molinfo-vienna/nerdd-backend/commit/7c548310a8071d82456c3ac14f95b06d1f925aa0))

* Merge pull request #16 from shirte/main

Adapt RethinkDbRepository ([`2117b36`](https://github.com/molinfo-vienna/nerdd-backend/commit/2117b36433f8ffd09291cd7e2a5fcdd04e87b3a3))

* Adapt RethinkdbRepository ([`9ec866b`](https://github.com/molinfo-vienna/nerdd-backend/commit/9ec866b71faca514017d09655b6f43ef5faeec10))

* Fix type in get_job_changes ([`b7905a5`](https://github.com/molinfo-vienna/nerdd-backend/commit/b7905a5156fee752ea5e3e3d98529f0774384d28))

* Delete default config file ([`2bbb16e`](https://github.com/molinfo-vienna/nerdd-backend/commit/2bbb16e7edce964f32a01ed0db8181ca9147f765))

* Merge pull request #15 from shirte/main

Many minor changes ([`7673a7e`](https://github.com/molinfo-vienna/nerdd-backend/commit/7673a7e79116ccc6e4eb0ad45e2b553091eb35a3))

* Use FileSystem class in sources router ([`a346546`](https://github.com/molinfo-vienna/nerdd-backend/commit/a346546495cf4b3cd26dc2e86b2ee8aaf1f3d6a6))

* Fix typo in SaveResultCheckpointToDb ([`188a883`](https://github.com/molinfo-vienna/nerdd-backend/commit/188a883c3c3c9d29549ee410e56cd26a907773d7))

* Add type stub package for aiofiles ([`aa14823`](https://github.com/molinfo-vienna/nerdd-backend/commit/aa1482331e6a70d5ca68703ebf7eac71e6a18530))

* Use global lock to avoid race conditions ([`23bd952`](https://github.com/molinfo-vienna/nerdd-backend/commit/23bd952cfd47d3a73a04793544618bcd5571eb9d))

* Make inputs and sources optional ([`2165f91`](https://github.com/molinfo-vienna/nerdd-backend/commit/2165f915d3bdc74c2315c4df6d1489bd451593f5))

* Implement route to return job output files ([`59057df`](https://github.com/molinfo-vienna/nerdd-backend/commit/59057df3be1aaa96af87bb14b539c8e307df19ec))

* Process serialization results ([`f847329`](https://github.com/molinfo-vienna/nerdd-backend/commit/f847329006dec91b38e41cabfe3b926dc7b32fb0))

* Hide route with slash suffix ([`7deab39`](https://github.com/molinfo-vienna/nerdd-backend/commit/7deab398cb3471d1074361375367c14ef02c5b7d))

* Provide output files in job model ([`60e22d3`](https://github.com/molinfo-vienna/nerdd-backend/commit/60e22d3b0f8d54d5e2ac6069cabd2f3bc82032dc))

* Add SerializeJobAction to mocked services ([`ad92c13`](https://github.com/molinfo-vienna/nerdd-backend/commit/ad92c13808f08576403cd5f7ba751399b1b93b4e))

* Fix typo in main ([`06a4eb0`](https://github.com/molinfo-vienna/nerdd-backend/commit/06a4eb0502581cd6b3959c398a768aa249842ca9))

* Remove InitializeAppLifespan ([`7fdf8db`](https://github.com/molinfo-vienna/nerdd-backend/commit/7fdf8dbba9a42568173baf3aa523013889532934))

* Add SaveResultCheckpointToDb action to main method ([`054b821`](https://github.com/molinfo-vienna/nerdd-backend/commit/054b8210bfc23bdc2f0df5da368e8e64c2600610))

* Adapt jobs router to repository ([`5d6c08e`](https://github.com/molinfo-vienna/nerdd-backend/commit/5d6c08e7868a0f085c5184b8c324551e32d8a493))

* Adapt sources router to repository ([`89ec5e1`](https://github.com/molinfo-vienna/nerdd-backend/commit/89ec5e1443df43cc8105fcd6c40bfa1c5578e1c5))

* Creation methods in repository return the inserted database objects ([`41a94d8`](https://github.com/molinfo-vienna/nerdd-backend/commit/41a94d8d37f376e7a8f03f8b60007aec93ec0e59))

* Adapt SaveResultToDb action to repository ([`96b1d67`](https://github.com/molinfo-vienna/nerdd-backend/commit/96b1d67f51115fe346f17ecacf46e5702b96881c))

* Adapt UpdateJobSize action to repository ([`db7644b`](https://github.com/molinfo-vienna/nerdd-backend/commit/db7644ba5a46f85e6c7dda25cbbab7527a7b329f))

* Implement SaveResultCheckpointToDb action ([`d22709b`](https://github.com/molinfo-vienna/nerdd-backend/commit/d22709be25d8c95205acf3e087edc7b327f397ef))

* Adapt SaveModuleToDb to repository ([`edb9836`](https://github.com/molinfo-vienna/nerdd-backend/commit/edb9836d61d0444528d01bc2e42a35b48dc1ea24))

* Adapt sources router to repository ([`1f54b84`](https://github.com/molinfo-vienna/nerdd-backend/commit/1f54b84b14edc0c3ffcd452ef5afba55d20a8307))

* Adapt repository to JobInternal and JobUpdate ([`64a2162`](https://github.com/molinfo-vienna/nerdd-backend/commit/64a216206217c31813e241efc5bb0b318a495bb7))

* Create additional JobInternal and JobUpdate models ([`c997266`](https://github.com/molinfo-vienna/nerdd-backend/commit/c9972666cdf3e83fe0a6c9659bd39cef00f5bbf6))

* Add test to check response list length ([`2aad149`](https://github.com/molinfo-vienna/nerdd-backend/commit/2aad149e46027af73a45f50034e7bc224a576fe3))

* Mock infrastructure when testing ([`88a2e5b`](https://github.com/molinfo-vienna/nerdd-backend/commit/88a2e5b709debb96705e24f5198ea3668a7027ab))

* Differentiate create from update operations in repository ([`a3bda46`](https://github.com/molinfo-vienna/nerdd-backend/commit/a3bda4604beabfd6f3b17201c5479356a5fb4b96))

* Add all output formats to config ([`25fed8c`](https://github.com/molinfo-vienna/nerdd-backend/commit/25fed8ce4d3fb9b5980f67035d6b43e82759592b))

* Add RecordAlreadyExistsException ([`5777985`](https://github.com/molinfo-vienna/nerdd-backend/commit/57779855fad8c051c8a85f428b74852dd25517f8))

* Merge pull request #14 from shirte/main

Add extra models ([`dafefdc`](https://github.com/molinfo-vienna/nerdd-backend/commit/dafefdcf7661d38a14e8167a4ea58baced942fa4))

* Adapt tests ([`d17881c`](https://github.com/molinfo-vienna/nerdd-backend/commit/d17881c7ee2bd06c790d91279e462b08b279640a))

* Adapt dynamic routes ([`39bf797`](https://github.com/molinfo-vienna/nerdd-backend/commit/39bf797a4482d40560ffbe42117bf163d350e0f3))

* Adapt results router ([`fc5389e`](https://github.com/molinfo-vienna/nerdd-backend/commit/fc5389ef7330968dd7e0b922ebae6cd5e0eb7b6d))

* Adapt jobs router ([`75bb8c1`](https://github.com/molinfo-vienna/nerdd-backend/commit/75bb8c1a181f648183737ff22ff874b2abf07091))

* Return smaller versions of module when list requested ([`4200f8c`](https://github.com/molinfo-vienna/nerdd-backend/commit/4200f8c2767e63e3662baf3250199d69cbb1092a))

* Adapt sources router ([`05a3431`](https://github.com/molinfo-vienna/nerdd-backend/commit/05a3431e6a6e9f84c7dc16a5dbc92f49cd8d55a5))

* Create extra models ([`fe9ab0d`](https://github.com/molinfo-vienna/nerdd-backend/commit/fe9ab0dfd4cdc6fb1777bf7e5bd558b51ab13d69))

* Save number of checkpoint when getting job size ([`49b229f`](https://github.com/molinfo-vienna/nerdd-backend/commit/49b229f4c6d31aa84d7cf1752245d894fd4aa048))

* Add page size to job ([`dffa16c`](https://github.com/molinfo-vienna/nerdd-backend/commit/dffa16c9d25ae9d244a16db4cb501314069d8194))

* Move models into submodule ([`ad176da`](https://github.com/molinfo-vienna/nerdd-backend/commit/ad176dac2cd375383d2805eab143fa8ad575c6b7))

* Merge pull request #13 from shirte/main

Major update ([`6dfc46d`](https://github.com/molinfo-vienna/nerdd-backend/commit/6dfc46dae721ca027d7e2f07c406eba51f347715))

* Overwrite old Readme ([`f1e6671`](https://github.com/molinfo-vienna/nerdd-backend/commit/f1e66712e3bc6cecc9f30f15fd45b4bee62822dd))

* Add todos in tests ([`d286955`](https://github.com/molinfo-vienna/nerdd-backend/commit/d2869551e62de7c407c709104ec5e1d86b99591b))

* Adapt websockets to new repository behaviour ([`76eee44`](https://github.com/molinfo-vienna/nerdd-backend/commit/76eee446ba1a759a82203ad127ff528f01276ec7))

* Use job model in jobs router ([`5cc5682`](https://github.com/molinfo-vienna/nerdd-backend/commit/5cc56826ef9bbf372385813c3e6472f5e318487c))

* Export sources ssteps ([`99782ea`](https://github.com/molinfo-vienna/nerdd-backend/commit/99782eabbc75e77b593c3819d6ff5f636a1cfb89))

* Use app config in results router ([`266dd18`](https://github.com/molinfo-vienna/nerdd-backend/commit/266dd18913f14dcf6deacc5477e98f82013aeedd))

* Add logging to ActionLifespan ([`2232d98`](https://github.com/molinfo-vienna/nerdd-backend/commit/2232d980de950ba82c6aeffbcda6acc16e93ce18))

* Use CreateJobRequest when calling the create_job route ([`d0b56f2`](https://github.com/molinfo-vienna/nerdd-backend/commit/d0b56f28c6f56d2d4dbfbb3fc21b98d0f57b8233))

* Add test steps for sources ([`6af91f8`](https://github.com/molinfo-vienna/nerdd-backend/commit/6af91f85019f941ec89f5f774102576fa81b4d08))

* Adapt test features ([`7d4321f`](https://github.com/molinfo-vienna/nerdd-backend/commit/7d4321f40d36c82eaf8f6ed2629aac1b6afa85e7))

* Add option to mock infrastructure ([`bdc90f5`](https://github.com/molinfo-vienna/nerdd-backend/commit/bdc90f545dd45080211c8138e1d49f6fdd700c7b))

* Add testing configuration ([`7ea6ca9`](https://github.com/molinfo-vienna/nerdd-backend/commit/7ea6ca9066df0b1cb17d4474374fa7b24c9b400c))

* Fix typo in rethinkdb.yaml ([`42d2de0`](https://github.com/molinfo-vienna/nerdd-backend/commit/42d2de0bc9d4219ffc7fe0a5ba55e6401d29b0b9))

* Start channel when initializing app ([`dbfa860`](https://github.com/molinfo-vienna/nerdd-backend/commit/dbfa860552ec9fed5d414fc4cdee0b0f21d61be1))

* Fix changes methods in RethinkDbRepository ([`4b628d9`](https://github.com/molinfo-vienna/nerdd-backend/commit/4b628d932b81a83f57668e0c95fe6ba6e2ddc2dd))

* Add num_entries_total to job model ([`d5f9979`](https://github.com/molinfo-vienna/nerdd-backend/commit/d5f99793b0fd332734bff2feb129bd3370c54df7))

* Store filename provided by user in db record ([`2b6c9d6`](https://github.com/molinfo-vienna/nerdd-backend/commit/2b6c9d6464135da642b32944de4a3491c620bd52))

* Remove unnecessary imports ([`f3f5bef`](https://github.com/molinfo-vienna/nerdd-backend/commit/f3f5bef833c133c95f04efb764c72a634b135c86))

* Fix types in actions ([`dfb3b0b`](https://github.com/molinfo-vienna/nerdd-backend/commit/dfb3b0b92e9cd6073aafcbb0e45f0228406857e9))

* Add types in MemoryRepository ([`61d9fea`](https://github.com/molinfo-vienna/nerdd-backend/commit/61d9feaea7e6bf7d9ecc38dd37c0dbbe336e3443))

* Add SaveResultsToDb action ([`a94df86`](https://github.com/molinfo-vienna/nerdd-backend/commit/a94df86390f29c80cfecd75cfffb7e12995cc098))

* Remove SaveJobToDb action ([`97a79bc`](https://github.com/molinfo-vienna/nerdd-backend/commit/97a79bc4f97d6126b1051461c3065bdbb7244a05))

* Use jsonable encoder before writing json file ([`541e85f`](https://github.com/molinfo-vienna/nerdd-backend/commit/541e85f25eea000b7efc4ed4e562dd0943312cd4))

* Merge pull request #12 from shirte/main

Minor changes ([`03dbfd3`](https://github.com/molinfo-vienna/nerdd-backend/commit/03dbfd383a138e211d1c982652709e4db55c4cf4))

* Implement changefeed methods in MemoryRepository ([`ff4e9d9`](https://github.com/molinfo-vienna/nerdd-backend/commit/ff4e9d916fddddc8f2b294c090791f363862aea3))

* Add correct types for ..._changes() methods in repository ([`8c7fa46`](https://github.com/molinfo-vienna/nerdd-backend/commit/8c7fa46106e99b549ff7a0dce13843a8010a35c8))

* Donot close CreateModuleLifespan on record error ([`3081409`](https://github.com/molinfo-vienna/nerdd-backend/commit/3081409a80e41664241a1c37af7f92e12b724c00))

* Improve code for checking if job record exists ([`0d26e9d`](https://github.com/molinfo-vienna/nerdd-backend/commit/0d26e9de9e8a6858fc090c98c79d81bb17e3a91c))

* Add request parameter to source handlers ([`0bf6842`](https://github.com/molinfo-vienna/nerdd-backend/commit/0bf684295d9d19c66d391f122c830322782217a5))

* Add option to mock infrastructure ([`175ca19`](https://github.com/molinfo-vienna/nerdd-backend/commit/175ca19a43e79ff2928a4d82dce4ad696ada9eee))

* Adapt dynamic router to Module type ([`5de0cc8`](https://github.com/molinfo-vienna/nerdd-backend/commit/5de0cc8931fc10518286e69cb9251bc05523933b))

* Merge pull request #11 from shirte/main

Add types and make id a required field ([`60ec44f`](https://github.com/molinfo-vienna/nerdd-backend/commit/60ec44f2873b71a6e5b568d55ae5c4be1da974d8))

* Add types in RethinkDbRepository ([`7d18da8`](https://github.com/molinfo-vienna/nerdd-backend/commit/7d18da887c05bc733686adcee1d5bf5599955835))

* Assume that id fields are always populated in MemoryRepository ([`04e7465`](https://github.com/molinfo-vienna/nerdd-backend/commit/04e746592558bcb8627d5ef58c7defe83063d5ec))

* Use computed_field in Module model class ([`ebee554`](https://github.com/molinfo-vienna/nerdd-backend/commit/ebee554aaf890b57edd59ef38ae42ac2752f0428))

* Make id a required field in model classes ([`d4493d6`](https://github.com/molinfo-vienna/nerdd-backend/commit/d4493d6bc1dc4fdc62ec50d1663b1c74923f56fd))

* Merge pull request #10 from shirte/main

Minor changes ([`38d271d`](https://github.com/molinfo-vienna/nerdd-backend/commit/38d271d0699618c16f76aadecd4484a1b6461f95))

* Raise exception instead of returning None in RethinkDbRepository ([`f8be5bf`](https://github.com/molinfo-vienna/nerdd-backend/commit/f8be5bf5ca5eb9835ee308e248426d4633a9ca34))

* Raise exception instead of returning None in memory_repository ([`843bdee`](https://github.com/molinfo-vienna/nerdd-backend/commit/843bdee24de995f9954f34dd0283f8e45df1a24d))

* Add submodule for exception classes ([`82c3a72`](https://github.com/molinfo-vienna/nerdd-backend/commit/82c3a725d3d8e5b3ab21f879bc294e8cac99318e))

* Add fake media directory in gitignore ([`c597cf3`](https://github.com/molinfo-vienna/nerdd-backend/commit/c597cf3d72f9708fc94522982b0674095d6dd46d))

* Use media_root from hydra config in sources router ([`dc53a56`](https://github.com/molinfo-vienna/nerdd-backend/commit/dc53a5605c3382b0af2eb325e27ec7a5425d4851))

* Add types in MemoryRepository ([`018e160`](https://github.com/molinfo-vienna/nerdd-backend/commit/018e160b769d46cb1842227a95bace8f57b84f02))

* Fix types in repository base class ([`6ef72fe`](https://github.com/molinfo-vienna/nerdd-backend/commit/6ef72fededa3d86bef49e1dc1873076076cb88da))

* Introduce create_app method for improved testing ([`09929c5`](https://github.com/molinfo-vienna/nerdd-backend/commit/09929c5109734b83f5ff64db444ba476dcb3c0ab))

* Use current date as initialization for created_at fields ([`fe77371`](https://github.com/molinfo-vienna/nerdd-backend/commit/fe773712ce81c0b5ce9c2c12d27a71f5e6f3f1a0))

* Replace setting variables in RethinkDbRepository ([`8601296`](https://github.com/molinfo-vienna/nerdd-backend/commit/8601296673708eff8e4f7ea769c4a0790ed6f212))

* Merge pull request #9 from shirte/main

Use hydra for managing settings ([`ddf6f4a`](https://github.com/molinfo-vienna/nerdd-backend/commit/ddf6f4ad2dfb6e8943fb7bcdb348c49dbcfc3458))

* Remove old setting variables from routers ([`00848b8`](https://github.com/molinfo-vienna/nerdd-backend/commit/00848b8c95b2b7f50ac01a7863bde2b8632ba7ac))

* Integrate hydra config in fast api ([`62dad3e`](https://github.com/molinfo-vienna/nerdd-backend/commit/62dad3ea4628da5a50a38afa0b902d625f523117))

* Move DummyRepository to non-test code ([`47f7f79`](https://github.com/molinfo-vienna/nerdd-backend/commit/47f7f7956d1c1c1789d6f643b6fafae2113cb5cf))

* Use hydra for managing configurations ([`3cf57c8`](https://github.com/molinfo-vienna/nerdd-backend/commit/3cf57c860c30fd37270bbed7df6162a0eabbb4cd))

* Make sources api use media root variable ([`783f74b`](https://github.com/molinfo-vienna/nerdd-backend/commit/783f74b440bed32301b98416e1197f9860e7dbfe))

* Merge pull request #8 from shirte/main

Introduce pydantic models for repository classes ([`d8476fa`](https://github.com/molinfo-vienna/nerdd-backend/commit/d8476fa6dea8c9422a887fd0580e6640c8f4dff5))

* Adapt RethinkDbRepository to model classes ([`5758184`](https://github.com/molinfo-vienna/nerdd-backend/commit/57581845f9da2848547fbb52ac65300f08346d5d))

* Finalize module feature test ([`c738517`](https://github.com/molinfo-vienna/nerdd-backend/commit/c738517f32d6e11dc65db342c6eeebb7f536b091))

* Export model classes in data.__init__ ([`a03558b`](https://github.com/molinfo-vienna/nerdd-backend/commit/a03558b65173807fde5b08b82e715d299395beae))

* Add test method to check partial responses ([`e7b15d9`](https://github.com/molinfo-vienna/nerdd-backend/commit/e7b15d977699fc07af767ac8dd40ec4883b01806))

* Adapt save_module_to_db action to model types ([`018bf5b`](https://github.com/molinfo-vienna/nerdd-backend/commit/018bf5b8228183a60133262288b472b50b919bb4))

* Adapt json repository class to model types ([`0cf9714`](https://github.com/molinfo-vienna/nerdd-backend/commit/0cf97145259493135f1f0564f06148e0d637026a))

* Adapt repository base class to model tyypes ([`1fe9c47`](https://github.com/molinfo-vienna/nerdd-backend/commit/1fe9c472c69a92aa61ca760e5af68841a051d4d4))

* Add module model ([`cd7bcc3`](https://github.com/molinfo-vienna/nerdd-backend/commit/cd7bcc33a5af8ca5f68f97deb04faa1fef4aa510))

* Add source model ([`82e5058`](https://github.com/molinfo-vienna/nerdd-backend/commit/82e50584c914d2eac12904bb27038dbb9f08a1d7))

* Add result model ([`03919b0`](https://github.com/molinfo-vienna/nerdd-backend/commit/03919b003c5c9ce1223d90605ef6e0fecacc4016))

* Add job model ([`352ba1a`](https://github.com/molinfo-vienna/nerdd-backend/commit/352ba1ab261932fabb7cdc02334f0580a31e5d97))

* Rename main test file ([`bea4a83`](https://github.com/molinfo-vienna/nerdd-backend/commit/bea4a837f33fc37d94569a4e8a79998741ccd685))

* Move request steps to client steps ([`4e509ac`](https://github.com/molinfo-vienna/nerdd-backend/commit/4e509ac36d5f47eefae92fe1ee35d9ef3c747f8c))

* Format code ([`c2d1361`](https://github.com/molinfo-vienna/nerdd-backend/commit/c2d1361899c9657e60c04f05970ad85d03f963d8))

* Fix all linting errors ([`138d992`](https://github.com/molinfo-vienna/nerdd-backend/commit/138d99235b5abcb46d509c9191a7ad21ba7e49a5))

* Move async_step to steps folder ([`b6b4f7b`](https://github.com/molinfo-vienna/nerdd-backend/commit/b6b4f7bf44b41661002923573b4eba4116972c57))

* Rename mocks folder to steps ([`081888b`](https://github.com/molinfo-vienna/nerdd-backend/commit/081888b02a7e410b547132fb6036a643bd53bcb9))

* Merge pull request #7 from shirte/main

Add testing code ([`92ee5e7`](https://github.com/molinfo-vienna/nerdd-backend/commit/92ee5e7e3546ec718126742934159d53fcf784ec))

* Add test features ([`1df20db`](https://github.com/molinfo-vienna/nerdd-backend/commit/1df20db1efb1d1f7337a7e6718aedb21c1215d2d))

* Implement test request steps ([`126b20c`](https://github.com/molinfo-vienna/nerdd-backend/commit/126b20ce219a9afba07d8eec24c29f70ee8bb635))

* Add init modules ([`6f61875`](https://github.com/molinfo-vienna/nerdd-backend/commit/6f618756232194a7427e051797f083d5f3475e07))

* Implement fake repository for tests ([`e2f86b4`](https://github.com/molinfo-vienna/nerdd-backend/commit/e2f86b43e89e5727048fb0dd951b7588bced23f0))

* Add fake test client ([`1fab588`](https://github.com/molinfo-vienna/nerdd-backend/commit/1fab588a79ec569a3b4aa2b65d09a136f38d21d0))

* Use dummy channel from nerdd-link ([`ea2f5c5`](https://github.com/molinfo-vienna/nerdd-backend/commit/ea2f5c5570583e2df8995bdf1e01fcafd1db3532))

* Add async step helper function ([`cfbc64d`](https://github.com/molinfo-vienna/nerdd-backend/commit/cfbc64d282bb3d19194776c87c5cd96fe6df7298))

* Add test configuration ([`e7742dd`](https://github.com/molinfo-vienna/nerdd-backend/commit/e7742dd86d6863800e5386bda73833cd029ab516))

* Add abstract repository class ([`ba622bf`](https://github.com/molinfo-vienna/nerdd-backend/commit/ba622bf1c82d2530d314b4a7194a5f194c334223))

* Add additional conda dependencies ([`2046434`](https://github.com/molinfo-vienna/nerdd-backend/commit/2046434630e54f948fbd6601ea9e3d0c1d38e3dc))

* Rewrite route handlers to use app state ([`aa9262d`](https://github.com/molinfo-vienna/nerdd-backend/commit/aa9262d0f5c4e158073801d26fa1c30906ed2892))

* Delete kafka result consumer ([`7148348`](https://github.com/molinfo-vienna/nerdd-backend/commit/714834845839eeb6063c8d4bcab9514f63d85ec5))

* Rewrite main ([`e3e96ac`](https://github.com/molinfo-vienna/nerdd-backend/commit/e3e96acac120bb83cc7bdc971ba201d130e6a213))

* Avoid using a singleton for the repository ([`99d7e9d`](https://github.com/molinfo-vienna/nerdd-backend/commit/99d7e9d8c265735f51e0613824acec8728678f61))

* Merge pull request #6 from shirte/main

Use nerdd-link for communication ([`50bc4b8`](https://github.com/molinfo-vienna/nerdd-backend/commit/50bc4b8a986d662721ad25482035cae9ea186928))

* Rewrite lifespans ([`374ecaa`](https://github.com/molinfo-vienna/nerdd-backend/commit/374ecaaf35580501a6c58112fd40c2a09417f7ed))

* Use nerdd-link actions for communication ([`618d042`](https://github.com/molinfo-vienna/nerdd-backend/commit/618d042a7aace5d22ca6d9b966baf96caba55ed2))

* Remove kafka consumer classes ([`b38c8ae`](https://github.com/molinfo-vienna/nerdd-backend/commit/b38c8ae315bcef70ad2ca9be7edb7bdf63dad5d3))

* Upgrade aiokafka dependency ([`f5cefb2`](https://github.com/molinfo-vienna/nerdd-backend/commit/f5cefb2c57c406933648b6362501506bce41fba1))

* Move py.typed file to correct dir ([`7a536d8`](https://github.com/molinfo-vienna/nerdd-backend/commit/7a536d8f6ef8f18bd0ae371515f07f64cbb81b1d))

* Move pytest config to pyproject.toml ([`bd84afb`](https://github.com/molinfo-vienna/nerdd-backend/commit/bd84afb0452b12383d9662723555264d024b78fd))

* Format code ([`9f5507f`](https://github.com/molinfo-vienna/nerdd-backend/commit/9f5507f49ba41973c61f500906b80b82fe6d7403))

* Fix pytest-bdd version ([`0ec2d0f`](https://github.com/molinfo-vienna/nerdd-backend/commit/0ec2d0f79961bbbf3244602c2cb6f6f215e17652))

* Add pytyped file ([`21aa024`](https://github.com/molinfo-vienna/nerdd-backend/commit/21aa0249a598ce363b2dbe6edadfb478ecf6626d))

* Convert setup.py to pyproject.toml ([`8a8a631`](https://github.com/molinfo-vienna/nerdd-backend/commit/8a8a631f8fa9231afcb2fb2d2579e43501f96abf))

* Add ruff to gitignore ([`dfd3dc1`](https://github.com/molinfo-vienna/nerdd-backend/commit/dfd3dc1dc3d30739cc2a0a65fe03d6cc63e51d97))

* Merge pull request #5 from shirte/main

Add settings submodule ([`a1897fb`](https://github.com/molinfo-vienna/nerdd-backend/commit/a1897fb0e788f39e5e5200974e2e79cb429dd08c))

* Add settings submodule ([`1d90b8c`](https://github.com/molinfo-vienna/nerdd-backend/commit/1d90b8c6c4869d103236b35a6502727c4be30a4b))

* Merge pull request #4 from shirte/main

Add code ([`ce85803`](https://github.com/molinfo-vienna/nerdd-backend/commit/ce858036d05c83240104853463a8716128175dbb))

* Add fastapi entrypoint ([`d8164da`](https://github.com/molinfo-vienna/nerdd-backend/commit/d8164da7056de468b072f05e992eea47f8a007f8))

* Add websocket router ([`6841a6c`](https://github.com/molinfo-vienna/nerdd-backend/commit/6841a6ca87b21532248e9d056b59d41a6e1952a0))

* Add REST routers ([`a3a0888`](https://github.com/molinfo-vienna/nerdd-backend/commit/a3a088872b3753f402d0f7249f1e291ce15440c1))

* Merge pull request #3 from shirte/main

Add code ([`66a3b37`](https://github.com/molinfo-vienna/nerdd-backend/commit/66a3b3728ee1b75701a1b0263e293b2d142f2b2a))

* Add lifespans ([`2e8f49c`](https://github.com/molinfo-vienna/nerdd-backend/commit/2e8f49c4bc455fe6516453df05720b55bd0e0cc9))

* Add consumers ([`743c6d9`](https://github.com/molinfo-vienna/nerdd-backend/commit/743c6d99cbd725a1600d2b81b2ce31d7a1719737))

* Add version module ([`1095ddd`](https://github.com/molinfo-vienna/nerdd-backend/commit/1095ddd3e302dbd07714fc4a113dd178a04d0e90))

* Add repository abstraction ([`3408a02`](https://github.com/molinfo-vienna/nerdd-backend/commit/3408a025802c78a7f3234727121fcec04da61f59))

* Merge pull request #2 from shirte/main

Add kafka consumers ([`207a37f`](https://github.com/molinfo-vienna/nerdd-backend/commit/207a37ffeb15c75d8a5738c2ecf86f3132cb4007))

* Add kafka consumers ([`6f7b92e`](https://github.com/molinfo-vienna/nerdd-backend/commit/6f7b92e488f726f2003134daa379a430d8b923fe))

* Merge pull request #1 from shirte/main

Add basic files ([`ada3773`](https://github.com/molinfo-vienna/nerdd-backend/commit/ada37734d6db94199858776843ecc52804a72853))

* Add requirements.txt ([`03273d2`](https://github.com/molinfo-vienna/nerdd-backend/commit/03273d23b122b635bcefbdf717b5890610cb4e2a))

* Add setup.py ([`e3d27dc`](https://github.com/molinfo-vienna/nerdd-backend/commit/e3d27dc6d7c9303333376043308ec345ae21ece3))

* Add environment yml ([`99f9649`](https://github.com/molinfo-vienna/nerdd-backend/commit/99f964905d87382053478f90f8a02c06f6bd8c1e))

* Add pytest config ([`97594e6`](https://github.com/molinfo-vienna/nerdd-backend/commit/97594e6b74cadd6e6853452a7ffb266ff2aca0ea))

* Add gitignore ([`43dcc7e`](https://github.com/molinfo-vienna/nerdd-backend/commit/43dcc7e5c218bbe9d5a44d7b0b1732d1ea2dd6dd))

* Initial commit ([`662d0c3`](https://github.com/molinfo-vienna/nerdd-backend/commit/662d0c3f7dc1fc4b6c64d83c75a6108f7a845a8e))

* Initial commit ([`2c0e4e5`](https://github.com/molinfo-vienna/nerdd-backend/commit/2c0e4e510bf03b45afaee6ae694dd59763eae40f))
