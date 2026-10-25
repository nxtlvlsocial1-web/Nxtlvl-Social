import { createHmac, timingSafeEqual } from 'node:crypto';

/** The X-Hub-Signature-256 value Meta sends with every webhook POST. */
export function signBody(body: Uint8Array | string, secret: string): string {
  return 'sha256=' + createHmac('sha256', secret).update(body).digest('hex');
}

export function isValidSignature(body: Uint8Array, header: string | null, secret: string): boolean {
  if (!header) return false;
  return safeEqual(signBody(body, secret), header);
}

export function safeEqual(a: string, b: string): boolean {
  const left = Buffer.from(a);
  const right = Buffer.from(b);
  return left.length === right.length && timingSafeEqual(left, right);
}

/**
 * Parses the signed_request Meta posts to the deauthorize and data-deletion callbacks.
 * Returns the payload, or undefined when the signature doesn't match.
 */
export function parseSignedRequest(signedRequest: string, secret: string): Record<string, unknown> | undefined {
  const [signature, payload] = signedRequest.split('.', 2);
  if (!signature || !payload) return undefined;
  const expected = createHmac('sha256', secret).update(payload).digest('base64url');
  if (!safeEqual(expected, signature.replace(/=+$/, ''))) return undefined;
  try {
    return JSON.parse(Buffer.from(payload, 'base64url').toString('utf8'));
  } catch {
    return undefined;
  }
}
