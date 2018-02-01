%%Plot rescaled densities for the Newton method on LJ potential.
v = VideoWriter('SelfSimilarDavidenko(LJP)', 'Motion JPEG AVI');
v.FrameRate = 12;
v.Quality = 100;
open(v);
timesteps = 240;
%TheMovie(timesteps) = struct('cdata', [], 'colormap', []);
for i=1:timesteps
    plot(DavidenkoPositions, DavidenkoDensity(i, :))
    xlabel('Position'); ylabel('Density');
    title(['Iteration ' num2str(i - 1)]);
    ylim([0, 15]);
    frame = getframe(gcf);
    writeVideo(v, frame);
end
close(v);