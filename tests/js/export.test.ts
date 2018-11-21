import "isomorphic-fetch";

import * as extension from '../../src/index';

describe('Checks exports', () => {
  test("Check extension", () => {
     expect(extension);
  });
});
