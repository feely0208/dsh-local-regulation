import * as faceapi from 'face-api.js';

export type VerifyResult = { ok: boolean; score: number };

/**
 * 门店闸机：从摄像头画面里检测一张人脸并生成特征描述。
 * 返回值只用于当次通行判断，不落库。
 */
export async function verifyMemberFace(video: HTMLVideoElement): Promise<VerifyResult> {
  const detection = await faceapi.detectSingleFace(video);
  if (!detection) return { ok: false, score: 0 };

  const descriptor = await faceapi.computeFaceDescriptor(video);
  return { ok: true, score: descriptor.length };
}
