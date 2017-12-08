%%Plot rescaled densities for the Newton method on LJ potential.
v = VideoWriter('SelfSimilarNewton(LJP)', 'Motion JPEG AVI');
v.FrameRate = 12;
v.Quality = 100;
open(v);
timesteps = 120;
%TheMovie(timesteps) = struct('cdata', [], 'colormap', []);
for i=1:timesteps
    plot(Positions, Density(i, :))
    xlabel('Position'); ylabel('Density');
    ylim([0, 40]);
    frame = getframe(gcf);
    writeVideo(v, frame);
end
close(v);